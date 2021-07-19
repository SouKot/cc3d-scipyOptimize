from cc3d import CompuCellSetup
from nutrient_stress_mitosisSteppables import ConstraintInitializerSteppable
from nutrient_stress_mitosisSteppables import GrowthSteppable
from nutrient_stress_mitosisSteppables import MitosisSteppable
from nutrient_stress_mitosisSteppables import DeathSteppable


def configure_simulation():
    from cc3d.core.XMLUtils import ElementCC3D

    CompuCell3DElmnt = ElementCC3D(
        "CompuCell3D", {"Revision": "20200724", "Version": "4.2.2"}
    )
    pg = CompuCellSetup.persistent_globals
    MetadataElmnt = CompuCell3DElmnt.ElementCC3D("Metadata")
    MetadataElmnt.ElementCC3D("NumberOfProcessors", {}, "1")
    MetadataElmnt.ElementCC3D("DebugOutputFrequency", {}, "100")
    PottsElmnt = CompuCell3DElmnt.ElementCC3D("Potts")
    PottsElmnt.ElementCC3D("Dimensions", {"x": "256", "y": "256", "z": "1"})
    PottsElmnt.ElementCC3D("Steps", {}, str(int(pg.input_object[9])))
    PottsElmnt.ElementCC3D("Temperature", {}, "10.0")
    PottsElmnt.ElementCC3D("NeighborOrder", {}, "1")
    PluginElmnt = CompuCell3DElmnt.ElementCC3D("Plugin", {"Name": "CellType"})
    PluginElmnt.ElementCC3D("CellType", {"TypeId": "0", "TypeName": "Medium"})
    PluginElmnt.ElementCC3D("CellType", {"TypeId": "1", "TypeName": "senCell"})
    PluginElmnt.ElementCC3D("CellType", {"TypeId": "2", "TypeName": "tolCell"})
    CompuCell3DElmnt.ElementCC3D("Plugin", {"Name": "Volume"})
    CompuCell3DElmnt.ElementCC3D("Plugin", {"Name": "CenterOfMass"})
    PluginElmnt_1 = CompuCell3DElmnt.ElementCC3D("Plugin", {"Name": "Contact"})
    PluginElmnt_1.ElementCC3D("Energy", {"Type1": "Medium", "Type2": "Medium"}, "10.1")
    PluginElmnt_1.ElementCC3D("Energy", {"Type1": "Medium", "Type2": "tolCell"}, "5.0")
    PluginElmnt_1.ElementCC3D("Energy", {"Type1": "Medium", "Type2": "senCell"}, "5.0")
    PluginElmnt_1.ElementCC3D(
        "Energy", {"Type1": "tolCell", "Type2": "tolCell"}, "-5.0"
    )
    PluginElmnt_1.ElementCC3D("Energy", {"Type1": "tolCell", "Type2": "senCell"}, "4.1")
    PluginElmnt_1.ElementCC3D("Energy", {"Type1": "senCell", "Type2": "senCell"}, "7.1")
    PluginElmnt_1.ElementCC3D("NeighborOrder", {}, "4")
    CompuCell3DElmnt.ElementCC3D("Plugin", {"Name": "NeighborTracker"})
    SteppableElmnt = CompuCell3DElmnt.ElementCC3D(
        "Steppable", {"Type": "DiffusionSolverFE"}, " -->"
    )
    DiffusionFieldElmnt = SteppableElmnt.ElementCC3D(
        "DiffusionField", {"Name": "NUTRIENT"}
    )
    DiffusionDataElmnt = DiffusionFieldElmnt.ElementCC3D("DiffusionData")
    DiffusionDataElmnt.ElementCC3D("FieldName", {}, "nutrient")
    DiffusionDataElmnt.ElementCC3D("GlobalDiffusionConstant", {}, "25")
    DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant", {}, "0.0")
    DiffusionDataElmnt.ElementCC3D("InitialConcentrationExpression", {}, "5.5")
    DiffusionDataElmnt.ElementCC3D(
        "DiffusionCoefficient", {"CellType": "senCell"}, "18"
    )
    DiffusionDataElmnt.ElementCC3D("DiffusionCoefficient", {"CellType": "tolCell"}, "8")
    DiffusionDataElmnt.ElementCC3D("DecayCoefficient", {"CellType": "senCell"}, "0.1")
    DiffusionDataElmnt.ElementCC3D("DecayCoefficient", {"CellType": "tolCell"}, "0.04")
    BoundaryConditionsElmnt = DiffusionFieldElmnt.ElementCC3D("BoundaryConditions")
    PlaneElmnt = BoundaryConditionsElmnt.ElementCC3D("Plane", {"Axis": "X"})
    PlaneElmnt.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Min", "Value": "0.0"}
    )
    PlaneElmnt.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Max", "Value": "0.0"}
    )
    PlaneElmnt_1 = BoundaryConditionsElmnt.ElementCC3D("Plane", {"Axis": "Y"})
    PlaneElmnt_1.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Min", "Value": "0.0"}
    )
    PlaneElmnt_1.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Max", "Value": "0.0"}
    )
    DiffusionFieldElmnt_1 = SteppableElmnt.ElementCC3D(
        "DiffusionField", {"Name": "STRESS"}
    )
    DiffusionDataElmnt_1 = DiffusionFieldElmnt_1.ElementCC3D("DiffusionData")
    DiffusionDataElmnt_1.ElementCC3D("FieldName", {}, "stress")
    DiffusionDataElmnt_1.ElementCC3D("GlobalDiffusionConstant", {}, "14")
    DiffusionDataElmnt_1.ElementCC3D("InitialConcentrationExpression", {}, "0.0")
    DiffusionDataElmnt_1.ElementCC3D(
        "DiffusionCoefficient", {"CellType": "senCell"}, "22"
    )
    DiffusionDataElmnt_1.ElementCC3D(
        "DiffusionCoefficient", {"CellType": "tolCell"}, "22"
    )
    DiffusionDataElmnt_1.ElementCC3D("DecayCoefficient", {"CellType": "senCell"}, "0.0")
    DiffusionDataElmnt_1.ElementCC3D(
        "DecayCoefficient", {"CellType": "tolCell"}, "0.005"
    )
    SecretionDataElmnt = DiffusionFieldElmnt_1.ElementCC3D("SecretionData")
    SecretionDataElmnt.ElementCC3D(
        "SecretionOnContact",
        {"SecreteOnContactWith": "tolCell", "Type": "tolCell"},
        "0.015",
    )
    SecretionDataElmnt.ElementCC3D(
        "SecretionOnContact",
        {"SecreteOnContactWith": "senCell", "Type": "tolCell"},
        "0.05",
    )
    SecretionDataElmnt.ElementCC3D(
        "SecretionOnContact",
        {"SecreteOnContactWith": "senCell", "Type": "senCell"},
        "0.04",
    )
    SecretionDataElmnt.ElementCC3D(
        "SecretionOnContact",
        {"SecreteOnContactWith": "tolCell", "Type": "senCell"},
        "-0.15",
    )
    BoundaryConditionsElmnt_1 = DiffusionFieldElmnt_1.ElementCC3D("BoundaryConditions")
    PlaneElmnt_2 = BoundaryConditionsElmnt_1.ElementCC3D("Plane", {"Axis": "X"})
    PlaneElmnt_2.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Min", "Value": "0.0"}
    )
    PlaneElmnt_2.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Max", "Value": "0.0"}
    )
    PlaneElmnt_3 = BoundaryConditionsElmnt_1.ElementCC3D("Plane", {"Axis": "Y"})
    PlaneElmnt_3.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Min", "Value": "0.0"}
    )
    PlaneElmnt_3.ElementCC3D(
        "ConstantDerivative", {"PlanePosition": "Max", "Value": "0.0"}
    )
    SteppableElmnt_1 = CompuCell3DElmnt.ElementCC3D(
        "Steppable", {"Type": "BlobInitializer"}
    )
    RegionElmnt = SteppableElmnt_1.ElementCC3D("Region")
    RegionElmnt.ElementCC3D("Center", {"x": "128", "y": "128", "z": "0"})
    RegionElmnt.ElementCC3D("Radius", {}, "40")
    RegionElmnt.ElementCC3D("Gap", {}, "7")
    RegionElmnt.ElementCC3D("Width", {}, "4")
    
    if pg.input_object[0] == 10:
        RegionElmnt.ElementCC3D("Types", {}, "tolCell")
    elif pg.input_object[0] == 20 :
        RegionElmnt.ElementCC3D("Types", {}, "senCell")
    elif pg.input_object[0] == 11:
        RegionElmnt.ElementCC3D("Types", {}, "tolCell,senCell")
    elif pg.input_object[0] == 14:
        RegionElmnt.ElementCC3D("Types", {}, "senCell,tolCell,tolCell,tolCell,tolCell")
    elif pg.input_object[0] == 41:
        RegionElmnt.ElementCC3D("Types", {}, "senCell,senCell,senCell,senCell,tolCell")

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)


configure_simulation()
CompuCellSetup.register_steppable(steppable=ConstraintInitializerSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=DeathSteppable(frequency=1))
CompuCellSetup.run()
