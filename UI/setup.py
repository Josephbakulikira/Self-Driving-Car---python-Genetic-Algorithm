from UI.ui import *
from constants import *

panel = Panel()
quitSave = Button("Save and Quit")
quitSave.w = 200
quitSave.position = (Width-280, 450)
quitSave.border = 0

GenerationText = TextUI("Generation: ", (Width//2 - 100, Height//2 - 120), (255, 255, 255), "topleft")
PopulationText = TextUI("population size: ", (Width//2 - 100, Height//2 - 80), (255, 255, 255), "topleft")
AgentAliveText = TextUI("agent Alive: ", (Width//2 - 100, Height//2 - 40), (255, 255, 255), "topleft")
HighestFitnessText = TextUI("Highest Fitness Score: ", (Width//2 - 100, Height//2), (255, 255, 255), "topleft")

editorModeText = TextUI(  "EditorMode :",      (Width-350, 100), (255, 255, 255), "topleft")
editText = TextUI("Start Editing :",           (Width-350, 140), (255, 255, 255), "topleft")
wireframeModeText = TextUI("Wireframe :",      (Width-350, 180), (255, 255, 255), "topleft")
showLineText = TextUI("Boundary: ", (Width-350, 220), (255, 255, 255), "topleft")

TrackWidthText = TextUI("Track Width: ", (Width-320, 270), (255, 255, 255), "topleft")


editorModeToggle = ToggleButton((Width-200, 100), 20, 20, False)
editToggle = ToggleButton((Width-200, 140), 20, 20, False)
wireframeToggle = ToggleButton((Width-200, 180), 20, 20, False)
ShowlineToggle  = ToggleButton((Width-200, 220), 20, 20, False)

WidthSlider = Slider(Width-205, 275, TRACK_WIDTH, 10, 120, 150, 10)
