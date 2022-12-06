import Tkinter,gradint
gradint.justSynthesize="zh "+Tkinter.Tk().selection_get(selection="CLIPBOARD").encode("utf-8").replace("#","")
# gradint.just_synthesize()
gradint.GUI_translations["Cancel lesson"]={"en":"Press here to cancel this reading"}
gradint.main()
