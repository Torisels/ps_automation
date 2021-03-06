const positions = {1: [800, 628], 2: [432, 894, 2080, 398], 3: [211, 923, 1246, 585, 2319, 383]}
const scales = {1: [100], 2: [40, 40], 3: [38, 38, 38]}


const collection_name = "HFB03";


/*Preserve settings*/
var original_unit = preferences.rulerUnits;
var original_type_unit = preferences.typeUnits;
var original_display_dialogs = app.displayDialogs;
/*******************/
#include
"json2.js"


// var file_to_read = File(app.activeDocument.path + "/result.json");
var file_to_read = File("C:\\Users\\Gustaw\\PycharmProjects\\ikea_generator\\result.json");
// var file_to_read = File("C:\\Users\\Gustaw\\PycharmProjects\\ikea_generator\\numbers.json");
var input_json = null;
var content;
if (file_to_read !== false) {// if it is really there
    file_to_read.open('r'); // open it
    content = file_to_read.read(); // read it
    input_json = JSON.parse(content);// now evaluate the string from the file
    file_to_read.close(); // always close files after reading
//
} else {
    alert("Error when reading JSON file!"); // if something went wrong
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
};

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

// var file_to_read = File(app.activeDocument.path + "/current_state.txt");
// file_to_read.open('r'); // open it
// content = file_to_read.read(); // read it
// file_to_read.close(); // always close files after reading
// var n = parseInt(content) + 1;
// // var n = 0;
// // n = 9;
// // for (var k = n; k < n + 1; k++) {
// //     var products = input_json[k]
// //     var product_count = products.length;
// //
// //     var f = new File(app.activeDocument.path + "/"+products[0].psd_name);
// //     app.open(f);
// //     for (var i = 0; i < product_count; i++) {
// //         var product = products[i]
// //         var set = app.activeDocument.layerSets.getByName("product" + (i + 1).toString());
// //
// //
// //
// //         var code_layer = set.layers.getByName("code");
// //         code_layer.textItem.contents = product.ikea_id;
// //
// //
// //
// //     }
// //     var SaveFile = File(app.activeDocument.path + "/" + products[0].new_name+".psd");
// //     if (SaveFile.exists) {
// //         SaveFile.remove();
// //     }
// //     SavePSD(SaveFile);
// //     saveTxt(n);
// // }
// for (var k = n; k < n + 1; k++) {
//     var products = input_json[k]
//     var product_count = products.length;
//     // alert(product_count);
//     var adder = "";
//     if (product_count == 1) {
//         if (products[0].more_options == false) {
//             adder = "_nmo";
//         }
//     }
//
//
//     if (products[0].lower == true) {
//         adder += "_lower";
//     }
//
//
//     if (products[0].lines == 2) {
//         adder += "_2lines";
//     }
//
//     var eee = app.activeDocument.path + "/template_" + product_count + adder + ".psd"
//     alert(eee);
//
//
//     var f = new File(app.activeDocument.path + "/template_" + product_count + adder + ".psd");
//
//     app.open(f);
//     for (var i = 0; i < product_count; i++) {
//         var product = products[i]
//         var set = app.activeDocument.layerSets.getByName("product" + (i + 1).toString());
//         var availableNowLayer = app.activeDocument.layers.getByName("availablenow" + (i + 1).toString());
//         var specialOfferLayer = app.activeDocument.layers.getByName("specialOffer" + (i + 1).toString());
//
//         var price_layer = set.layers.getByName("price");
//         price_layer.textItem.contents = product.price_string;
//
//         var name_layer = set.layers.getByName("name");
//         name_layer.textItem.contents = product.name;
//
//         var code_layer = set.layers.getByName("code");
//         code_layer.textItem.contents = product.ikea_id;
//
//         var desc_layer = set.layers.getByName("description");
//         desc_layer.textItem.contents = product.description;
//
//
//         // var logoFile = app.activeDocument.path + "/input_photos/" + collection_name + "/" + product.file_name; // Watermark file should be large for resize down works better than up
//         var logoFile = "E:\\IKEA_ALL_PICS\\Pictures for packshots - per team\\" + product.collection_name + "\\" + product.file_name; // Watermark file should be large for resize down works better than up
//         var LogoSize = scales[product_count][i]; // percent of document height to resize Watermark to
//         var xpos = positions[product_count][2 * i];
//         var ypos = positions[product_count][2 * i + 1];
//
//         placeImage(logoFile, LogoSize, xpos, ypos);
//
//         if (product.special_offer == true) {
//             specialOfferLayer.visible = true;
//             availableNowLayer.visible = false;
//         } else {
//             specialOfferLayer.visible = false;
//             availableNowLayer.visible = true;
//         }
//
//     }
//     var SaveFile = File(app.activeDocument.path + "/" + products[0].psd_name);
//     if (SaveFile.exists) {
//         SaveFile.remove();
//     }
//     SavePSD(SaveFile);
//     saveTxt(n);
// }
var product_count = app.activeDocument.layerSets.length;
for (var i = 0; i < product_count; i++) {
        var set = app.activeDocument.layerSets.getByName("product" + (i + 1).toString());
        var code_layer = set.layers.getByName("price");
        var text_price = code_layer.textItem.contents.split("\r")
        var juan = text_price[1].split(" ")[1]
        var usd = text_price[2].split(" ")[1]
        var text = text_price[0]+"\r(US) " + juan + " USD\r" + "(CN) " + usd + " CNY";
        code_layer.textItem.contents = text;

    }

var SaveFile = File(app.activeDocument.path + "/" + app.activeDocument.name);
    if (SaveFile.exists) {
        SaveFile.remove();
    }
    SavePSD(SaveFile);


// var doc = app.activeDocument;
// var fileName = doc.name.split('.')[0];
// var collection_name = fileName.split('_')[2];
// app.displayDialogs = DialogModes.NO;
// var jpgOptions = new JPEGSaveOptions();
// jpgOptions.quality = 12;
// jpgOptions.embedColorProfile = true;
// jpgOptions.formatOptions = FormatOptions.PROGRESSIVE;
// jpgOptions.scans = 5;
// jpgOptions.matte = MatteType.NONE;
//
// doc.saveAs(new File(app.activeDocument.path + '/Results_JPG/' + collection_name + "/" + fileName + '.jpg'), jpgOptions);
// //doc.close();
//
// app.displayDialogs = DialogModes.YES;


// for(var i = 0 ; i <=2; i++)
// {
//      var set = app.activeDocument.layerSets.getByName("product" + (i + 1).toString());
// var code_layer = set.layers.getByName("code");
//
//
//
// var desc_layer = set.layers.getByName("description");
// desc_layer.textItem.contents += "\r"+code_layer.textItem.contents;
// code_layer.textItem.contents = "";
//
// }

// app.activeDocument.close();
//
//
// var doc = app.activeDocument;
// var fileName = doc.name.split('.')[0];
// app.displayDialogs = DialogModes.NO;
// var jpgOptions = new JPEGSaveOptions();
// jpgOptions.quality = 12;
// jpgOptions.embedColorProfile = true;
// jpgOptions.formatOptions = FormatOptions.PROGRESSIVE;
// jpgOptions.scans = 5;
// jpgOptions.matte = MatteType.NONE;
//
// doc.saveAs(new File( app.activeDocument.path + '/Results_JPG/' + fileName + '.jpg'), jpgOptions);
// doc.close();
//
// /*Restore settings*/
// preferences.rulerUnits = 