import vtk
import numpy as np

def interpolate_vectors(data, point):
    points = vtk.vtkPoints()
    points.InsertNextPoint(point)
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    
    probe = vtk.vtkProbeFilter()
    probe.SetInputData(polydata)
    probe.SetSourceData(data)
    probe.Update()
    
    output = probe.GetOutput()
    if output is None:
        print("No output for probe filter")
        return None
    
    vectors = output.GetPointData().GetVectors()
    if vectors is None:
        print("No vectors found")
        return None
    
    interpolated_vector = vectors.GetTuple3(0)
    return interpolated_vector


def rk4_integration(data, seed, step_size, max_steps):
    streamline = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    streamline.SetPoints(points)
    lines = vtk.vtkCellArray()
    streamline.SetLines(lines)

    current_point = list(seed)
    points.InsertNextPoint(current_point)

    for _ in range(max_steps):
        interpolated_vector = interpolate_vectors(data, current_point)
        if interpolated_vector is None:
            print("Failed to interpolate", current_point)
            break

        a = np.array(interpolated_vector) * step_size

        half_point_b = [current_point[i] + a[i] / 2 for i in range(3)]
        interpolated_vector_b = interpolate_vectors(data, half_point_b)
        if interpolated_vector_b is None:
            print("Failed to interpolate vector at half point B", half_point_b)
            break
        b = np.array(interpolated_vector_b) * step_size

        half_point_c = [current_point[i] + b[i] / 2 for i in range(3)]
        interpolated_vector_c = interpolate_vectors(data, half_point_c)
        if interpolated_vector_c is None:
            print("Failed to interpolate vector at half point C", half_point_c)
            break
        c = np.array(interpolated_vector_c) * step_size

        end_point_d = [current_point[i] + c[i] for i in range(3)]
        interpolated_vector_d = interpolate_vectors(data, end_point_d)
        if interpolated_vector_d is None:
            print("Failed to interpolate vector at end point D", end_point_d)
            break
        d = np.array(interpolated_vector_d) * step_size

        new_point = [current_point[i] + (a[i] + 2 * b[i] + 2 * c[i] + d[i]) / 6 for i in range(3)]

        current_point = new_point
        points.InsertNextPoint(current_point)
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, points.GetNumberOfPoints() - 2)
        line.GetPointIds().SetId(1, points.GetNumberOfPoints() - 1)
        lines.InsertNextCell(line)

    return streamline

def main():
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("tornado3d_vector.vti")
    reader.Update()
    data = reader.GetOutput()

    print("Enter seed location : ")
    numbers = list(map(float, input().split()))
    seed_location = np.array(numbers)

    step_size = 0.05
    max_steps = 1000
    forward_streamline = rk4_integration(data, seed_location, step_size, max_steps)
    backward_streamline = rk4_integration(data, seed_location, -step_size, max_steps)

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    for i in range(forward_streamline.GetNumberOfPoints()):
        points.InsertNextPoint(forward_streamline.GetPoint(i))
    for i in range(backward_streamline.GetNumberOfPoints()):
        points.InsertNextPoint(backward_streamline.GetPoint(i))

    for i in range(forward_streamline.GetNumberOfCells()):
        cell = forward_streamline.GetCell(i)
        lines.InsertNextCell(cell)

    offset = forward_streamline.GetNumberOfPoints()
    for i in range(backward_streamline.GetNumberOfCells()):
        cell = backward_streamline.GetCell(i)
        new_cell = vtk.vtkLine()
        new_cell.GetPointIds().SetId(0, cell.GetPointId(0) + offset)
        new_cell.GetPointIds().SetId(1, cell.GetPointId(1) + offset)
        lines.InsertNextCell(new_cell)

    combined_streamline = vtk.vtkPolyData()
    combined_streamline.SetPoints(points)
    combined_streamline.SetLines(lines)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("streamline.vtp")
    writer.SetInputData(combined_streamline)
    writer.Write()

if __name__ == "__main__":
    main()
