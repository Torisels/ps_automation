function saveTxt(txt) {
    var Path = app.activeDocument.path;
    var saveFile = File(Path + "/current_state.txt");

    if (saveFile.exists)
        saveFile.remove();

    saveFile.encoding = "UTF8";
    saveFile.open("e", "TEXT", "????");
    saveFile.writeln(txt);
    saveFile.close();
}



saveTxt("-1");