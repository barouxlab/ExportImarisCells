#  PythonXT Simple Segmentation Export Example for Imaris
#  
#
#  Copyright Bitplane AG
#
#
#    <CustomTools>
#      <Menu>
#       <Item name="Export Segmentation" icon="Python" tooltip="Simple XTension overloading the Volume scene with segmented bits">
#         <Command>PythonXT::CreateSegmentationMask(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>
import ImarisLib

def GetServer():
  vImarisLib = ImarisLib.ImarisLib()
  vServer = vImarisLib.GetServer()
  return vServer;

def get_imaris():
  lib = ImarisLib.ImarisLib()
  server = lib.GetServer()
  num_objects = server.GetNumberOfObjects()
  if (num_objects > 0):
    imaris_id = server.GetObjectID(0)
  imaris = lib.GetApplication(imaris_id)
  return imaris


def get_cells(imaris):
  selection = imaris.GetSurpassSelection()
  cells = imaris.GetFactory().ToCells(selection)
  return cells


def add_mask(all_mask, index, single_mask):
  for row in range(len(all_mask)):
    for col in range(len(all_mask[0])):
      for depth in range(len(all_mask[0][0])):
        all_mask[row][col][depth]= all_mask[row][col][depth] + ((index + 1)*single_mask[row][col][depth])
      

def create_allcell_mask(cells):
  num_cells = cells.GetNumberOfCells()
  #print 'Number of cells: ' + str(num_cells)
  c = 0
  t = 0
  all_mask = cells.GetCell(0).GetDataVolumeFloats(c, t)
  for index in range(1, num_cells):
    single_mask = cells.GetCell(index).GetDataVolumeFloats(c, t)
    add_mask(all_mask, index, single_mask)
  return all_mask




def main():
  imaris = get_imaris()
  dataset = imaris.GetDataSet()
  cells = get_cells(imaris)

  all_mask = create_allcell_mask(cells)
  z = 0
  c = 0
  t = 0
  dataset.SetSizeC(1)
  dataset.SetSizeT(1)

  dataset = imaris.GetDataSet()
  dataset.SetDataVolumeBytes(all_mask, c, t)
  
if __name__ == "__main__":
  main()
