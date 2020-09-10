// Adobe Premiere Simple Slideshow Generator

main();

function sort_by_name(a, b) {
    if (a.name > b.name)
        return 1;
    return -1;
}

function main() {

    var photo_name = "KMP20-001";
    var to_search = photo_name;
    var sequence_name1 =photo_name;

// have the user select a folder where their images are located
    var importFolder = new Folder("E:\\Ikea_Projekt\\Results_JPG\\360\\" + photo_name);


    var files = importFolder.getFiles();

// no files were found. rerun script and tell user to select a valid folder
    if (files.length < 1) {
        alert("No files detected", "Select a valid folder");
        main();
    }

// gets the paths for all the images in the folder
    var imageFiles = getImagePaths(files);

// if there are no image files in the folder, have the user to try again
    if (imageFiles.length < 1) {
        alert("No image files in this folder", "Try again!");
        main();
    }

// let the user decide how many seconds each image will be
    var seconds = 0.15;

// project setup
    var project = app.project;
    var projectItem = project.rootItem;

// import the files we found earlier
    project.importFiles(imageFiles);

// create a Bin called "Image Folder"
    var imageFolder = projectItem.createBin("Folder" + sequence_name1);


    var seq = null;
//project.sequences[0].clone();
    for (var i = 0; i < project.sequences.length; i++) {
        seq = project.sequences[i];
        if (seq.name === to_search) {
            break;
        }
    }
//seq.clone();
    seq.name = photo_name;

//for (var i = 0; i<project.sequences.length; i++)
//{
    // seq = project.sequences[i];
    //if (seq.name === "source_sequence_xxx Copy")
    // {
    // break;
    //}
//}
// after importing our images, we need to locate them in the project
    var importedImages = getImageProjectItems(projectItem);

    importedImages.sort(sort_by_name)


// get the first video track (where all the images will be)
    var videoTrackOne = seq.videoTracks[1];

    var time = new Time();
    time.ticks = seq.timebase.toString();

    var frameLength = time.seconds;
    var startTime = 0;

// create a new time object for easier calculations later
    var thisTime = new Time();
    thisTime.seconds = parseFloat(seconds);


    for (var e = 0; e < importedImages.length; e++) {
        importedImages[e].moveBin(imageFolder); 
        videoTrackOne.insertClip(importedImages[e], startTime);
        startTime += parseFloat(seconds) ;
        try {
            videoTrackOne.clips[e].end = videoTrackOne.clips[e].start.seconds + parseFloat(seconds);
        } catch (e) {
        }
    }


// get all the images that were inserted to the sequence
    var trackItems = getTrackClips(videoTrackOne);

    for (var i = 0; i < trackItems.length; i++) {
// get effect objects of the current image
        var components = trackItems[i].components;

// [motionObj, opacityObj]
        var videoComponentObjs = getComponentObjs(components);

// adjust opacity (add keys too)
        var opacityParam = videoComponentObjs[1].opacity;
        videoComponentObjs[0].scale.setValue(45);



//videoComponentObjs[0].position.setValue([0.45, 0.42 ]);
//videoComponentObjs[0].position.setValue([0.45, 0.42 ]);
    }
}

function animateScale(param, length, image, scale, seconds) {
    // allow keyframes
    param.setTimeVarying(true);
    // add a keyframe at the beginning, and end of the image (for scale)
    param.addKey(image.inPoint.seconds);
    param.addKey(image.inPoint.seconds + seconds);

    // change those keyframes to be the original value, and original value  + 10%
    param.setValueAtKey(image.inPoint.seconds, scale);
    param.setValueAtKey(image.inPoint.seconds + seconds, scale * 1.1);
}

function fadeOpacity(param, length, image, seconds) {
    // allow keyframes
    param.setTimeVarying(true);
    // add keyframes at beginning and end of the image layer (for opacity)
    param.addKey(image.inPoint.seconds);
    param.addKey(image.inPoint.seconds + length);
    param.addKey(image.inPoint.seconds + seconds - length);
    param.addKey(image.inPoint.seconds + seconds);

    // change the keyframes to be 0 and 100
    param.setValueAtKey(image.inPoint.seconds, 0);
    param.setValueAtKey(image.inPoint.seconds + length, 100);
    param.setValueAtKey(image.inPoint.seconds + seconds - length, 100);
    param.setValueAtKey(image.inPoint.seconds + seconds, 0);
}

function getComponentObjs(components) {
    var opacityComponent;
    var motionComponent;
    // search for the opacity and motion components for this given image
    var motionObj = {};

    for (var i = 0; i < components.numItems; i++) {
        if (components[i].displayName === "Opacity") {
            opacityComponent = components[i];
        }
        if (components[i].displayName === "Motion") {
            motionComponent = components[i];
        }
    }

    var opacityObj = {
        opacity: opacityComponent.properties[0]
    };
// once the opacity and motion components are found, we need to get the other values (like position, scale, rotation, etc.)
    for (var e = 0; e < motionComponent.properties.numItems; e++) {
        switch (motionComponent.properties[e].displayName) {
            case "Position":
                var a = motionComponent.properties[e].getValue();
                motionObj.position = motionComponent.properties[e];
                break;
            case "Scale":
                motionObj.scale = motionComponent.properties[e];
                break;
            case "Scale Width":
                motionObj.scaleWidth = motionComponent.properties[e];
                motionObj.scaleCheck = motionComponent.properties[e + 1];
                break;
            case "Rotation":
                motionObj.rotation = motionComponent.properties[e];
                break;
            case "Anchor Point":
                motionObj.anchorPoint = motionComponent.properties[e];
                break;
        }
    }

    motionObj.scaleCheck.setValue(true, true);
    // send back a proprietary object that only we know the hierarchy of
    return [motionObj, opacityObj];
}

function getTrackClips(videoTrack) {
    var clips = [];
    // get all the clips from the current track
    for (var i = 0; i < videoTrack.clips.numItems; i++) {
        clips.push(videoTrack.clips[i]);
    }

    return clips;
}

function getImageProjectItems(projectItem) {
    var projectImages = [];
    var thisName;
// get all the image files in our project panel (jpg, jpeg, and png)
    for (var i = 0; i < projectItem.children.numItems; i++) {
        thisName = projectItem.children[i].name;
        if (thisName.substring(thisName.length - 3, thisName.length).toLowerCase() === "jpg") {
            projectImages.push(projectItem.children[i]);
        }
    }

    return projectImages;
}

function getImagePaths(files) {
    var thisName;
    var paths = [];
    for (var i = 0; i < files.length; i++) {
        thisName = files[i].name;
        if (thisName.substring(thisName.length - 3, thisName.length).toLowerCase() === "jpg") {
            paths.push(files[i].fsName);
        }
    }
    return paths;
}