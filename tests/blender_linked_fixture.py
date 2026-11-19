"""Create and verify an external-image fixture from inside Blender."""

import sys
from pathlib import Path

import bpy


def create(project, resource):
    resource.parent.mkdir(parents=True, exist_ok=True)
    generated = bpy.data.images.new("Fixture Pixel", width=1, height=1)
    generated.pixels[:] = (1, 0, 0, 1)
    generated.filepath_raw = str(resource)
    generated.file_format = "PNG"
    generated.save()
    bpy.data.images.remove(generated)

    image = bpy.data.images.load(str(resource))
    image.filepath = "//" + resource.relative_to(project.parent).as_posix()
    material = bpy.data.materials.new("Fixture Material")
    material.use_nodes = True
    texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    texture.image = image
    shader = material.node_tree.nodes.get("Principled BSDF")
    material.node_tree.links.new(texture.outputs["Color"], shader.inputs["Base Color"])
    cube = bpy.data.objects["Cube"]
    cube.data.materials.clear()
    cube.data.materials.append(material)
    assert "FINISHED" in bpy.ops.wm.save_as_mainfile(filepath=str(project), relative_remap=False)


def verify(project, resource):
    assert "FINISHED" in bpy.ops.wm.open_mainfile(filepath=str(project), load_ui=False, use_scripts=False)
    image = bpy.data.images[resource.name]
    assert Path(bpy.path.abspath(image.filepath)).resolve() == resource.resolve(), image.filepath
    image.reload()
    assert tuple(image.size) == (1, 1), tuple(image.size)


if __name__ == "__main__":
    action, project_path, resource_path = sys.argv[sys.argv.index("--") + 1:]
    operations = {"create": create, "verify": verify}
    operations[action](Path(project_path), Path(resource_path))
