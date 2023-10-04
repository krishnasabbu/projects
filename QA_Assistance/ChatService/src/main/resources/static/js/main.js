var userStartDiv = '<li class="message right"> <div class="message-box"> <div class="text">userTypedText</div> <div class="message-meta"><span class="message-time">userTypedTime</span> <span><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAASCAMAAAB7LJ7rAAAASFBMVEUAAAD////////////////////////////////////////////////////////////////////////////////////////////neHiwAAAAF3RSTlMA90sR79wiWTgYzqWMhLmunmzkZMMseO19QZoAAADBSURBVCjPfZFZEoMgEEQdFgVkNWrf/6ZhMWBZKfsLeDDdM0x/xNX0IhbFC7cbXL/5hNoT1ms9e/EsLAddCDLf1yNTEsA6t6cWMGpShj4/agkIR12rkGm2dgSRGo2Z7o2yHZA1mAdEeT/vAOTcbCWwsWYiAFq42jrlJ5Wjy/IDgGKhRvHUQoFSD7yiyTAdKLKyFedtFLJSuUwBoLIhx+/DIDQzR0CnQ8WtRvGVWv0YphGpt9GnOnS40UZ4+Wwe/b3yF6iHDCtvO97mAAAAAElFTkSuQmCC" alt="tick" /></span></div> </div> </li>';
var userEndDiv = '</div></div><div class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible"><button class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400 md:invisible md:group-hover:visible"><svg xmlns="http://www.w3.org/2000/svg" stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button></div><div class="flex justify-between"/></div></div></div>';

var chatStartDiv = '<div class="HeroCardBox"> <li class="message left"> <div class="message-box"> <div class="text" style="white-space: normal;"> botTypedText </div> <div class="message-meta"><span class="message-time">botTypedTime</span></div> </div> </li> </div>';
var chatEndDiv = '</div> </div> </div> <div class="flex justify-between"> <div class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible"> <button class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"> <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"> <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path> </svg> </button> <button class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"> <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"> <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path> </svg> </button> </div> </div> </div> </div> </div>';
var globalId = 0;
var globalIntent = "embeddings";

var applyButtonDiv = "<div class='quick-links'><div class='quick-link' id='applyCC' onclick='addImageButton()'><div class='link'>Apply</div></div></div>";
var imageButtonDiv = "<div id='image-upload'><input type='file' id='file-input' accept='image/*' /><img id='preview-image' src='#' alt='Preview Image' /><p id='drag-text'>Drag and drop image here or click to upload</p></div>";

var submitDiv = "<div id='creditCardSuccess'>Credit Card application processed sucessfully. Card will be sent to registered Address with in 5 business days. There are disclosures attached to the card. <br/> If you want to send it to your email, please enter below else continue. <br/> <input type='text' name='email'> <br/> </div>";
var submitDivLinks = "<div class='quick-links'> <div class='quick-link' id='finalSubmit'> <div class='link'>Submit </div> </div><div class='quick-link' id='finalContinue'> <div class='link'>Continue </div> </div> </div>";
var finalDiv = "<div style='padding: 10px;'>Email Sent Successfully..  Please check your inbox. <br/> Is there any thing else I may assist..</div>";

var attachDiv = "<div style='display:none'><div class='quick-links'><div class='quick-link' id='submitCard'><div class='link'>Apply</div></div></div></div>"

$(document).on('click', '#applyCC', function() {
   $(imageButtonDiv).insertBefore("#most-asked-questions");
   const bottomElement = document.getElementById('file-input');
   bottomElement.scrollIntoView({ behavior: "smooth" });
});

$(document).on('click', '#submitCC', function() {
    console.log("fired");
    fireSubmitCardCall('Email');
});

$(document).on('click', '#activeCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Active Cash Card. Please upload id proof to process further..');
});

$(document).on('click', '#biltCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Bilt Card. Please upload id proof to process further..');
});

$(document).on('click', '#autographCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Autograph Card. Please upload id proof to process further..');
});

$(document).on('click', '#reflectCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Reflect Card. Please upload id proof to process further..');
});

$(document).on('click', '#masterCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Master Card. Please upload id proof to process further..');
});

$(document).on('click', '#selectMasterCard', function() {
     console.log("fired");
     event.preventDefault();
     console.log("Fired");
     fireStaticCall('Thanks for choosing Wells Fargo Select Card. Please upload id proof to process further..');
});

$(document).on('click', '#finalSubmit', function() {
    console.log("fired");
    fireSubmitCardCall('final');
});

$(document).on('click', '#finalContinue', function() {
    console.log("fired");
    fireSubmitCardCall('finalContinue');
});

$(document).on('dragover', '#image-upload', function(event) {
   event.preventDefault();
   event.stopPropagation();
   console.log("Drag over.....")
   var imageUpload = $('#image-upload');
   console.log("imageUpload ==== "+imageUpload);
   document.getElementById('image-upload').classList.add('dragging');
   $(this).addClass("dragging");
});

$(document).on('dragleave', '#image-upload', function(event) {
   event.preventDefault();
   event.stopPropagation();
   document.getElementById('image-upload').classList.remove('dragging');
   $(this).removeClass("dragging");
});

$(document).on('drop', '#image-upload', function(event) {
   event.preventDefault();
   event.stopPropagation();
   $(this).removeClass("dragging");
   var file = event.originalEvent.dataTransfer.files[0];
   console.log("file === "+file);
   previewFile(file);
});

$(document).on('change', '#file-input', function() {
   var file = this.files[0];
   console.log("file === "+file);
   previewFile(file);
});

      // Preview the selected file
function previewFile(file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    const offscreen_canvas = new OffscreenCanvas(0, 0);
    const offscreen_canvas_context = offscreen_canvas.getContext("2d");
    reader.onload = function (event) {
        const reader_image = event.target.result;
        const image = new Image();
        image.onload = function () {
          offscreen_canvas.width = image.width;
          offscreen_canvas.height = image.height;
          offscreen_canvas_context.drawImage(image, 0, 0);
          offscreen_canvas.convertToBlob().then((blob) => {
            var customElement = $("<div>", {
                "css"   : {
                    "font-size"     : "20px",
                    "font-weight"   : "bold",
                    "text-align"    : "center",
                    "padding"       : "10px",
                    "color"         : "green"
                },
                "text"  : "Processing your information...."
            });
            $.LoadingOverlay("show", {
                image       : "",
                custom      : customElement
            });
            Tesseract.recognize(blob).then(function(result){
               console.log(result.text);
               firedlCall(result.text);
            });
          });
        };
        image.src = reader_image;
    };
    reader.onloadend = function() {
      $('#preview-image').attr('src', reader.result);
      $('#preview-image').css('display', 'block');
    }
}

$(document).ready(function() {
    $("#search-form").submit(function(event) {
        console.log("Fired");
        event.preventDefault();
        fireApiCall('false');
    });
    $("form").submit(function(){
      alert("Submitted");
    });

    $("#chatImageBot").click(function(event) {
        $("#mainChatBot").show();

    });

    $("#closeChat").click(function(event) {
         $("#mainChatBot").hide();
    });

    $("#link").click(function(event) {
         $("#mainChatBot").hide();
    });

    $("#language").on("click", function() {
        $("#embeddings").removeAttr("style");
        $("#trained").removeAttr("style");
        $(this).css("background", "#d71e28");
        $(this).css("color", "white");
        globalIntent = 'language';
    });

    $("#activeCard").on("click", function() {
         event.preventDefault();
         console.log("Fired");
         $("#msg-input").val('Wells Fargo Active Cash Card');
         fireApiCall('true');
    });



    /*$("#applyCC").on("click", function() {
         event.preventDefault();
         console.log("Text ............... ");
         addImageButton();
    });*/

    $("#trained").on("click", function() {
        $("#embeddings").removeAttr("style");
        $("#language").removeAttr("style");
        $(this).css("background", "#d71e28");
        $(this).css("color", "white");
        globalIntent = 'trained';
    });

    $("#mic-btn").click(function(event) {
        event.preventDefault();
        console.log("Fired");
        fireApiCall('false');
    });

    $("#englishConvert").click(function(event) {
        event.preventDefault();
        console.log("Fired Conversion call");
        fireConversionCall('EN');
    });

    $("#spanishConvert").click(function(event) {
        event.preventDefault();
        console.log("Fired Conversion call");
        fireConversionCall('SPN');
    });

    $("input[name$='chatGPTType']").click(function() {
        $("#userText").val('');
        $('#chat_empty_discussion').empty();
        $('#chat_empty_discussion').html('<div class="w-full h-32 md:h-48 flex-shrink-0" id="chat_discussion"></div>');
    });
});

function initialChat() {
    globalId = globalId + 1;
    var customId = "typing-effect" + globalId;
    var customTimeId = "typing-effect-time" + globalId;
    var paragraph = '<p id=' + customId + '></p>';
    var paragraphTime = '<p id=' + customTimeId + '></p>';
    var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
    var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
    console.log('finalChatDiv === '+finalChatDiv);
    var texteerw = "Hi Welcome to wells"
    $(texteerw).insertBefore("#most-asked-questions");
    var text = "Hi Welcome to Wellsfargo Bank";
    console.log(text);
    if (text.indexOf('<br/>') > 0) {
        text = '<pre>' + data.data + '</pre>';
    }
    var index = 0;
    var interval = setInterval(function() {
        $("#typing-effect" + globalId).html(text.slice(0, index++));
        if (index > text.length) {
            clearInterval(interval);
        }
    }, 50);
    $("#typing-effect" + globalId).closest('div.result-streaming').removeClass('result-streaming markdown prose w-full break-words dark:prose-invert dark');
    $("#typing-effect-time" + globalId).html(formatAMPM(new Date));
}

function addApplyButton() {
    $(applyButtonDiv).insertBefore("#most-asked-questions");
}

function addImageButton() {
   /* $('#submitCC').show();*/
}

function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

console.log(formatAMPM(new Date));

function fireSubmitCardCall(type) {
    if(type == 'Email') {
      /*var insertText = "Thanks for applying credit card... <br/> <br/> Please enter your email id : <input type='text' name='email'>"
      var timeText = "<div class='quick-links'> <div class='quick-link' id='finalSubmit'> <div class='link'>Submit </div> </div> </div>";*/
      var paragraph = '<p id="submitSucc1"></p>';
      var paragraphTime = '<p id="submitSucc1Time"></p>';
      var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
      var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
      $(finalChatDiv).insertBefore("#most-asked-questions");
      var index = 0;
      var text = submitDiv;
      var interval = setInterval(function() {
          $("#submitSucc1").html(text.slice(0, index++));
          if (index > text.length) {
              clearInterval(interval);
              $(submitDivLinks).insertBefore("#most-asked-questions");
              $("#submitSucc1Time").html(formatAMPM(new Date));
          }
      }, 50);
    }

    if(type == 'final') {
      var insertText = "Email Sent Successfully..  Please check your inbox. <br/> <br/> Is there any thing else I may assist.."
      var timeText = "";
      var paragraph = '<p id="fianlSubmitcc"></p>';
      var paragraphTime = '<p id="fianlSubmitccTime"></p>';
        var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
        var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
        $(finalChatDiv).insertBefore("#most-asked-questions");
        var index = 0;
        var text = insertText;
        var interval = setInterval(function() {
            $("#fianlSubmitcc").html(text.slice(0, index++));
            if (index > text.length) {
                clearInterval(interval);
                $("#fianlSubmitccTime").html(formatAMPM(new Date));
            }
        }, 15);
    }

    if(type == 'finalContinue') {
      var insertText = "Is there any thing else I may assist.."
      var timeText = "";
      var paragraph = '<p id="assistCustom"></p>';
      var paragraphTime = '<p id="assistCustomTime"></p>';
      var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
      var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
      $(finalChatDiv).insertBefore("#most-asked-questions");
      var index = 0;
      var text = insertText;
      var interval = setInterval(function() {
          $("#assistCustom").html(text.slice(0, index++));
          if (index > text.length) {
              clearInterval(interval);
              $("#assistCustomTime").html(formatAMPM(new Date));
          }
      }, 15);
    }
}

function fireConversionCall(language) {
    var search = {}
    search["data"] = $("#msg-input").val();
    search["chatGPTType"] = 'language';
    search["language"] = language;
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/api/v1/chat1",
        data: JSON.stringify(search),
        dataType: 'json',
        cache: false,
        timeout: 600000,
        success: function(data) {
            $("#customConvertBody").html(data.data);
        },
        error: function(e) {
            var json = "<h4>Response From Model : </h4><pre>" +
                e.responseText + "</pre>";
            console.log(json);
        }
    });
}

function firedlCall(text) {
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/api/v1/dl",
        data: text,
        cache: false,
        timeout: 600000,
        success: function(data) {
            $.LoadingOverlay("hide");
            console.log("data === "+data);
            $(data).insertBefore("#most-asked-questions");
            $("#most-asked-questions").focus();
            const bottomElement = document.getElementById('submitCC');
            bottomElement.scrollIntoView({ behavior: "smooth" });
        },
        error: function(e) {
            var json = "<h4>Response From Model : </h4><pre>" +
                e.responseText + "</pre>";
            console.log(json);
        }
    });
}

function fireStaticCall(text) {
    globalId = globalId + 1;
    var customId = "typing-effect" + globalId;
    var customTimeId = "typing-effect-time" + globalId;
    var paragraph = '<p id=' + customId + '></p>';
    var paragraphTime = '<p id=' + customTimeId + '></p>';
    var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
    var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
    $(finalChatDiv).insertBefore("#most-asked-questions");
    $("#typing-effect" + globalId).focus();
    $("#msg-input").val('');
    const bottomElement1 = document.getElementById('file-input');
    bottomElement1.scrollIntoView({ behavior: "smooth" });
    console.log(text);
    if (text.indexOf('<br/>') > 0) {
        text = '<pre>' + data.data + '</pre>';
    }
    var index = 0;
    var interval = setInterval(function() {
        $("#typing-effect" + globalId).html(text.slice(0, index++));
        if (index > text.length) {
            clearInterval(interval);
            attachTime();
            $(imageButtonDiv).insertBefore("#most-asked-questions");
           const bottomElement = document.getElementById('file-input');
           bottomElement.scrollIntoView({ behavior: "smooth" });
        }
    }, 15);
    $("#typing-effect" + globalId).closest('div.result-streaming').removeClass('result-streaming markdown prose w-full break-words dark:prose-invert dark');
}

function fireApiCall(addButtons) {
    var search = {}
    search["data"] = $("#msg-input").val();
    search["chatGPTType"] = globalIntent;
    search["language"] = 'SPN';
    var userDiv = userStartDiv.replace('userTypedText', $("#msg-input").val());
    var finalUserDiv = userDiv.replace('userTypedTime', formatAMPM(new Date));
    $(finalUserDiv).insertBefore("#most-asked-questions");
    globalId = globalId + 1;
    var customId = "typing-effect" + globalId;
    var customTimeId = "typing-effect-time" + globalId;
    var paragraph = '<p id=' + customId + '></p>';
    var paragraphTime = '<p id=' + customTimeId + '></p>';
    var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
    var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
    $(finalChatDiv).insertBefore("#most-asked-questions");
    $("#typing-effect" + globalId).focus();
    $("#msg-input").val('');

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/api/v1/chat1",
        data: JSON.stringify(search),
        dataType: 'json',
        cache: false,
        timeout: 600000,
        beforeSend: function(){
            $.LoadingOverlay("show");
        },
        success: function(data) {
            $.LoadingOverlay("hide");
            var text = data.data;
            console.log(text);
            if (text.indexOf('<br/>') > 0) {
                text = '<pre>' + data.data + '</pre>';
            }
            var index = 0;
            console.log("text ========= "+text);
            var interval = setInterval(function() {
                $("#typing-effect" + globalId).html(text.slice(0, index++));
                console.log("index ========= "+index);
                console.log("text.length ========= "+text.length);
                if (index > text.length) {
                    clearInterval(interval);
                    attachTime();
                    if(addButtons == 'true') {
                        addApplyButton();
                    }
                    const bottomElement = document.getElementById('submitCard');
                    bottomElement.scrollIntoView({ behavior: "smooth" });
                }
            }, 15);
            $("#typing-effect" + globalId).closest('div.result-streaming').removeClass('result-streaming markdown prose w-full break-words dark:prose-invert dark');
            //$("#typing-effect-time" + globalId).html(formatAMPM(new Date));
        },
        error: function(e) {
            var json = "<h4>Response From Model : </h4><pre>" +
                e.responseText + "</pre>";
            console.log(e);
        }
    });
}

function attachTime() {
    $("#typing-effect-time" + globalId).html(formatAMPM(new Date));
}