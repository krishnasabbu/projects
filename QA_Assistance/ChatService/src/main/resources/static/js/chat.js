var chatStartDiv = '<div class="HeroCardBox"> <li class="message left"> <div class="message-box"> <div class="text" style="white-space: normal;"> botTypedText </div> <div class="message-meta"><span class="message-time">botTypedTime</span></div> </div> </li> </div>';
var chatEndDiv = '</div> </div> </div> <div class="flex justify-between"> <div class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible"> <button class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"> <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"> <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path> </svg> </button> <button class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"> <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"> <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path> </svg> </button> </div> </div> </div> </div> </div>';
var linksDiv = '<div class="quick-links"> <div class="quick-link" id="activeCard"> <div class="link">Wells Fargo Active Cash Card </div> </div> <div class="quick-link" id="visaCard"> <div class="link">Wells Fargo Cash Wise Visa Card </div> </div> <div class="quick-link" id="platinumCard"> <div class="link">Wells Fargo Platinum Card </div> </div> <div class="quick-link" id="rewardsCard"> <div class="link">Wells Fargo Rewards Card</div> </div> </div>';

$(document).ready(function() {
    $("#chatImageBot").click(function(event) {
       $("#mainChatBot").show();
       //initialChat();
    });

    $("#closeChat").click(function(event) {
         $("#mainChatBot").hide();
    });

    $("#link").click(function(event) {
         $("#mainChatBot").hide();
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
});

function initialChat() {
    var askedQ = $("#botId").contents().find("#most-asked-questions");
    globalId = 130;
    var customId = "typing-effect" + globalId;
    var customTimeId = "typing-effect-time" + globalId;
    var paragraph = '<p id=' + customId + '></p>';
    var paragraphTime = '<p id=' + customTimeId + '></p>';
    var chatDiv = chatStartDiv.replace('botTypedText', paragraph);
    var finalChatDiv = chatDiv.replace('botTypedTime', paragraphTime);
    //$(finalChatDiv).insertBefore(askedQ);
    //var text = "&#128512; Hello. I'm Wells. Welcome to Wellsfargo Credit Card Assistant! I'm here to answer any questions you might have about Credit Cards. Please Choose a card to continue..";
    var text1 = '<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3"> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Wells Fargo Active Cash® Card</h5> <ul class="card-text"> <li>$200 cash rewards bonus</li> <li>Unlimited 2% cash rewards</li> <li>0% intro APR for 15 months</li> <li>$0 annual fee</li> </ul> </div> </div> </div> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Bilt Mastercard®</h5> <ul class="card-text"> <li>Points on rent</li> <li>0 annual fee</li> <li>1X-6X points on various categories</li> <li>Double points on first of each month</li> </ul> </div> </div> </div> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Wells Fargo Autograph Card</h5> <ul class="card-text"> <li>20,000 bonus points</li> <li>0% intro APR for 12 months</li> <li>3X points on various categories</li> <li>$0 annual fee</li> </ul> </div> </div> </div> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Wells Fargo Reflect® Card</h5> <ul class="card-text"> <li>Lowest intro APR for 21 months</li> <li>0% intro APR for 18 months</li> <li>$0 annual fee</li> </ul> </div> </div> </div> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Choice Privileges® Mastercard® Credit Card</h5> <ul class="card-text"> <li>60,000 bonus points</li> <li>5X-3X points on various categories</li> <li>Up to 7 reward nights</li> <li>$0 annual fee</li> </ul> </div> </div> </div> <div class="col"> <div class="card h-100"> <div class="card-body"> <h5 class="card-title">Choice Privileges® Select Mastercard® Credit Card</h5> <ul class="card-text"> <li>90,000 bonus points</li> <li>10X-5X points on various categories</li> <li>Up to 11 reward nights</li> <li>$95 annual fee (waived first year)</li> </ul> </div> </div> </div></div>';
    var text = '<div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Active Cash Card </h4> </div> <div class="course-info"> <h6>$200 cash rewards bonus </h6> <h6>Unlimited 2% cash rewards </h6> <h6>0% intro APR for 15 months </h6> <h6>$0 annual fee </h6> </div> <button id="activeCard" class="cutomBtn">Apply </button> </div></div><div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Bilt Mastercard </h4> </div> <div class="course-info"> <h6>Points on rent </h6> <h6>0 annual fee </h6> <h6>1X-6X points on various categories </h6> <h6>Double points on first of each month </h6> </div> <button id="biltCard" class="cutomBtn">Apply </button> </div></div><div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Autograph Card </h4> </div> <div class="course-info"> <h6>20,000 bonus points </h6> <h6>0% intro APR for 12 months </h6> <h6>3X points on various categories </h6> <h6>$0 annual fee </h6> </div> <button id="autographCard" class="cutomBtn">Apply </button> </div></div><div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Reflect Card </h4> </div> <div class="course-info"> <h6>Lowest intro APR for 21 months </h6> <h6>0% intro APR for 18 months </h6> <h6>$0 annual fee </h6> </div> <button id="reflectCard" class="cutomBtn">Apply </button> </div></div><div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Mastercard </h4> </div> <div class="course-info"> <h6>60,000 bonus points </h6> <h6>5X-3X points on various categories </h6> <h6>Up to 7 reward nights </h6> <h6>$0 annual fee </h6> </div> <button id="masterCard" class="cutomBtn">Apply </button> </div></div><div class="courses-container"> <div class="course"> <div class="course-preview"> <h4>Wells Fargo Select Mastercard </h4> </div> <div class="course-info"> <h6>90,000 bonus points </h6> <h6>10X-5X points on various categories </h6> <h6>Up to 11 reward nights </h6> <h6>$95 annual fee (waived first year) </h6> </div> <button id="selectMasterCard" class="cutomBtn">Apply </button> </div></div>';
    $(text).insertBefore(askedQ);
    //$(text1).insertBefore(askedQ);
    //attachLinksDiv();
    /*var index = 0;
    var interval = setInterval(function() {
        $("#botId").contents().find("#typing-effect130").html(text.slice(0, index++));
        if (index > text.length) {
            clearInterval(interval);
            attachTime();
            attachLinksDiv();
        }
    }, 10);*/
    $("#botId").contents().find("#typing-effect130").closest('div.result-streaming').removeClass('result-streaming markdown prose w-full break-words dark:prose-invert dark');

}

function attachTime() {
    $("#botId").contents().find("#typing-effect-time130").html(format_AM_PM(new Date()));
}

function attachLinksDiv()  {
   var askedL = $("#botId").contents().find("#most-asked-questions");
   $(linksDiv).insertBefore(askedL);
}

function format_AM_PM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

function fireConversionCall(language) {
    var search = {}
    search["data"] = $("#msg-input").val();
    search["chatGPTType"] = 'language';
    search["language"] = language;
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/api/v1/chat",
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
