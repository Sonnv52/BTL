function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
  $("#textInput").val("");
  $("#chatbox").append(userHtml);
  var ok = 0
  document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
  $.get("/get", { message: rawText }).done(function (data) {
    $.each(data, function (name, val) {
      if (val >= 60) {
        var botHtml = '<p class="botText"><span>' + "Bạn có thể đã bị " + name + '</span></p>';
        $("#chatbox").append(botHtml);
        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
        ok = 1
      }
    })
    if (ok == 0){
      $.each(data, function (name, value) {
        var botHtml = '<p class="botText"><span>' + name + " " + value + "%" + '</span></p>';
        $("#chatbox").append(botHtml);
        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
      });
      $.get("/getPropose", { message: rawText }).done(function (data) {
        var botHtml = '<p class="botText"><span>' +"Bạn có còn các triệu trứng hay tiền sử: "+ data + '</span></p>';
        $("#chatbox").append(botHtml);
        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
      });
    }
  });
}
$("#textInput").keypress(function (e) {
  if (e.which == 13) {
    getBotResponse();
  }
});
$("#buttonInput").click(function () {
  getBotResponse();
})