# Script to load gradint's synthloop quickly without waiting for the GUI
import sys
sys.argv.append("useTk=0")
import gradint
gradint.primitive_synthloop()
