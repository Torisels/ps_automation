var collection_name = "HFB02";
var doc = app.activeDocument;
var fileName = doc.name.split('.')[0];
app.displayDialogs = DialogModes.NO;
var jpgOptions = new JPEGSaveOptions();
jpgOptions.quality = 12;
jpgOptions.embedColorProfile = true;
jpgOptions.formatOptions = FormatOptions.PROGRESSIVE;
jpgOptions.scans = 5;
jpgOptions.matte = MatteType.NONE;

doc.saveAs(new File(app.activeDocument.path + '/Results_JPG/' + collection_name + "/" + fileName + '.jpg'), jpgOptions);
doc.close();

app.displayDialogs = DialogModes.YES;