#! python 2.7
#    <CustomTools>
#      <Menu>
#       <Item name="Export Segmentation" icon="Python" tooltip="Simple XTension overloading the Volume scene with segmented bits">
#         <Command>PythonXT::createMaskDataSetFromCellStack(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>
import ImarisLib
import Imaris
import numpy as np
import time

def GetServer():
  vImarisLib = ImarisLib.ImarisLib()
  vServer = vImarisLib.GetServer()
  return vServer;

def get_first_imaris_from_server():
  lib = ImarisLib.ImarisLib()
  server = lib.GetServer()
  num_objects = server.GetNumberOfObjects()
  if (num_objects > 0):
    imaris_id = server.GetObjectID(0)
  imaris = get_imaris_by_ID(imaris_id)  
  return imaris

def get_imaris_by_ID(imarisId):
  lib = ImarisLib.ImarisLib()
  imaris = lib.GetApplication(imarisId)
  return imaris

def get_cells(imaris):
  selection = imaris.GetSurpassSelection()
  cells = imaris.GetFactory().ToCells(selection)
  return cells


#def add_mask(all_mask, index, single_mask):
#  for row in range(len(all_mask)):
#    for col in range(len(all_mask[0])):
#      for depth in range(len(all_mask[0][0])):
#        #all_mask[row][col][depth]= all_mask[row][col][depth] + (((index%(256-1)) + 1)*int(single_mask[row][col][depth]))
#        all_mask[row][col][depth]= all_mask[row][col][depth] + (((index+280))*int(single_mask[row][col][depth]))  

def create_allcell_mask(cells):
  num_cells = cells.GetNumberOfCells()
  print 'Number of cells: ' + str(num_cells)
  c = 0
  t = 0
  all_mask = cells.GetCell(0).GetDataVolumeFloats(c, t)
  all_mask = np.array(all_mask)
  for index in range(1, num_cells):
    single_mask = cells.GetCell(index).GetDataVolumeFloats(c, t)
    #print "I have applied the single mask"
    #all_mask += np.multiply(single_mask, (index%(256-1)+1))
    all_mask += np.multiply(single_mask, index+1)
    #print "I have added to all masks"
##    add_mask(all_mask, index, single_mask)
    print 'I am at cell: ' +str(index)
  return all_mask.tolist(), num_cells




def main():
  
  imaris = get_first_imaris_from_server()
  export_masks(imaris)
  
def export_masks(imaris):
  time.sleep(5)
  #imaris = get_imaris_by_ID(imarisId)

  # Check if the object is valid
  if imaris is None:
    print 'Could not connect to Imaris!'
  # Sleep 2 seconds to give the user a chance to see the printed message
    time.sleep(5)
    return

  dataset = imaris.GetDataSet()
  cells = get_cells(imaris)

  all_mask, num_cells = create_allcell_mask(cells)
  z = 0
  c = 0
  t = 0

  
  channelsSize = dataset.GetSizeC()
  print 'channel number is: ' + str(channelsSize)
  dataset.SetSizeC(channelsSize+1)
  dataset.SetSizeT(1)
  c = channelsSize
  dataset.SetChannelDescription(c, 'Channel of segmentation to be exported')
  dataset.SetChannelName(c, 'ExportSegmentation')
  ciccio = dataset.GetChannelColorTable(c)
  print ciccio
  #dataset.SetChannelColorTable(c, 1, 1, 2)
  #dataset.SetChannelRange(c, 0, 255)
##  dataset = imaris.GetDataSet()
  dataset.SetDataVolumeFloats(all_mask, c, t)

####sacha in Bitplane ####
  #create new dataset
  factory = imaris.GetFactory();
  newDataSet = factory.CreateDataSet()
  aType = Imaris.tType.eTypeUInt16
  aSizeX = dataset.GetSizeX();
  aSizeY = dataset.GetSizeY();
  aSizeZ = dataset.GetSizeZ();
  aSizeC = dataset.GetSizeC();
  aSizeT = 1;
  #we set the type of the dataset
  newDataSet.Create(aType, aSizeX, aSizeY, aSizeZ, 1, 1)
  
  newDataSet.SetDataVolumeFloats(all_mask, 0, t)
  newDataSet.SetChannelDescription(0, 'Channel of segmentation to be exported')
  newDataSet.SetChannelName(0, 'ExportSegmentation')
  #this will become the new active dataset
  imaris.SetDataSet(newDataSet)
  #imaris.FileSave('C:/mask.ims', 'writer=" Imaris5"');
  
  
def createMaskDataSetFromCellStack(imarisId):
  imaris = get_imaris_by_ID(imarisId)
  export_masks(imaris)
  
if __name__ == "__main__":
  main()
  
