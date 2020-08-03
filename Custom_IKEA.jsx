const positions = {1: [500, 200], 2: [300, 400, 2200, 400], 3: [300, 400, 2200, 400, 3000, 400]}
const scales = {1: [55], 2: [38, 45], 3: [40, 40, 45]}

/*Preserve settings*/
var original_unit = preferences.rulerUnits;
var original_type_unit = preferences.typeUnits;
var original_display_dialogs = app.displayDialogs;
/*******************/
#include
"json2.js"


var file_to_read = File(app.activeDocument.path + "/output.json");
var input_json = null;
var content;
if (file_to_read !== false) {// if it is really there
    file_to_read.open('r'); // open it
    content = file_to_read.read(); // read it
    input_json = JSON.parse(content);// now evaluate the string from the file
    file_to_read.close(); // always close files after reading
//
} else {
    alert("Bah!"); // if something went wrong
}


function createStringForPrices(eur, us, cn) {
    return "(DE) " + eur + " EUR\r" + "(US) " + us + " USD\r" + "(CN) " + cn + " CNY";
}

function SavePSD(saveFile) {
    var psdFile = new File(saveFile);
    psdSaveOptions = new PhotoshopSaveOptions();
    psdSaveOptions.embedColorProfile = true;
    psdSaveOptions.alphaChannels = true;
    activeDocument.saveAs(psdFile, psdSaveOptions, false, Extension.LOWERCASE);
}

function placeImage(Image, Size, x, y) {

    if (!documents.length) return;  // if no document return

    try {

        var doc = app.activeDocument; // set Doc object to active document
        app.displayDialogs = DialogModes.NO; // Dialog off
        app.preferences.rulerUnits = Units.PIXELS; // work with pixels
        app.preferences.typeUnits = TypeUnits.PIXELS; // work with pixels

        var fileObj = new File(Image);                 // the passed file
        if (!fileObj.exists) {  // If file does not exits tell user
            alert(fileObj.name + " does not exist!");
            return;
        }

        var layers = app.activeDocument.layers; // get layers

        app.activeDocument.activeLayer = layers[0] // Target Top Layer

        placeFile(fileObj); // Place in file the Watermark png file

        fileObj.close();

        activeDocument.activeLayer.resize(Size, Size, AnchorPosition.MIDDLECENTER); // Insure Place did not scale layer

        //var SB = activeDocument.activeLayer.bounds; // get layers bounds

        //var layerHeight = SB[3] - SB[1]; // get layers height

        //var resizePercent = (100 / layerHeight) * (Size / 100 * doc.height.value); // Percent to resize by

        //activeDocument.activeLayer.resize(40, 40, AnchorPosition.MIDDLECENTER);  // Resize width and height by percentage

        SB = activeDocument.activeLayer.bounds; // get resized layers bounds

        activeDocument.activeLayer.translate(-SB[0].value, -SB[1].value); // Move resized layer to top left canvas corner
        activeDocument.activeLayer.translate(x, y); // Move resized layer to top left canvas corner

        var docRef = app.activeDocument
        docRef.artLayers[0].move(docRef.artLayers[docRef.artLayers.length - 2], ElementPlacement.PLACEAFTER);
    } catch (e) {
        alert(e + ': on line ' + e.line);
    }
}

function placeFile(placeFile) {
    var desc21 = new ActionDescriptor();
    desc21.putPath(charIDToTypeID('null'), new File(placeFile));
    desc21.putEnumerated(charIDToTypeID('FTcs'), charIDToTypeID('QCSt'), charIDToTypeID('Qcsa'));

    var desc22 = new ActionDescriptor();
    desc22.putUnitDouble(charIDToTypeID('Hrzn'), charIDToTypeID('#Pxl'), 0.000000);
    desc22.putUnitDouble(charIDToTypeID('Vrtc'), charIDToTypeID('#Pxl'), 0.000000);

    desc21.putObject(charIDToTypeID('Ofst'), charIDToTypeID('Ofst'), desc22);
    executeAction(charIDToTypeID('Plc '), desc21, DialogModes.NO);
}

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

function saveDocumentAsJPGandClose() {
    var doc = app.activeDocument;
    var fileName = doc.name.split('.')[0];

    var jpgOptions = new JPEGSaveOptions();
    jpgOptions.quality = 12;
    jpgOptions.embedColorProfile = true;
    jpgOptions.formatOptions = FormatOptions.PROGRESSIVE;
    jpgOptions.scans = 5;
    jpgOptions.matte = MatteType.NONE;

    doc.saveAs(new File(app.activeDocument.path + '/Results_JPG/' + fileName + '.jpg'), jpgOptions);
    doc.close();
}

var file_to_read = File(app.activeDocument.path + "/current_state.txt");
file_to_read.open('r'); // open it
content = file_to_read.read(); // read it
file_to_read.close(); // always close files after reading
// var n = parseInt(content) + 1;
var n = 21;
// n = 9;
for (var k = n; k < n + 1; k++) {
    var products = input_json[k]
    var product_count = products.length;
    var f = new File(app.activeDocument.path + "/template_" + product_count + ".psd");
    app.open(f);
    for (var i = 0; i < product_count; i++) {
        var product = products[i]

        var set = app.activeDocument.layerSets.getByName("product" + (i + 1).toString());
        var price_layer = set.layers.getByName("price");
        price_layer.textItem.contents = createStringForPrices(product.eur, product.usd, product.cny);

        var name_layer = set.layers.getByName("name");
        name_layer.textItem.contents = product.name;

        var code_layer = set.layers.getByName("code");
        code_layer.textItem.contents = product.number;

        var desc_layer = set.layers.getByName("description");
        desc_layer.textItem.contents = product.desc;

        var logoFile = app.activeDocument.path + "/Dywany/" + product.file_name; // Watermark file should be large for resize down works better than up
        var LogoSize = scales[product_count][i]; // percent of document height to resize Watermark to
        var xpos = positions[product_count][2 * i];
        var ypos = positions[product_count][2 * i + 1];

        placeImage(logoFile, LogoSize, xpos, ypos);

    }
    var SaveFile = File(app.activeDocument.path + "/" + products[0].order_num + "_" + products[0].name + ".psd");
    if (SaveFile.exists) SaveFile.remove();
    SavePSD(SaveFile);
    saveTxt(n);
}

/*Restore settings*/
preferences.rulerUnits = original_unit;
preferences.typeUnits = original_type_unit;
app.displayDialogs = original_display_dialogs;
/******************/