<html>
<head>
<link rel="icon" type="image/ico" href="PandoraP.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
.button {
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
  background-color: white; 
  color: black; 
  border: 3px solid #1D329D;
}
.button:hover {
  background-color: #5A99F4;
  color: white;
  border: 3px solid white;
}
.setbutton {
  border: none;
  color: #1D519D;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
  background-color: #1D519D; 
  color: black; 
  border: 3px solid #5A99F4;
}
.setbutton:hover {
  background-color: #5A99F4;
  color: white;
  border: 3px solid white;
}


</style>
 <form align="right" method="post">
 <button type="submit" name="vdown" value="1" class="button"><img src="volume_down.svg" width="30" height="30"></button>
 <button type="submit" name="vup" value="1" class="button"><img src="volume_up.svg" width="30" height="30"></button>
 &ensp; &ensp; &ensp;
 <button type="submit" name="stationlist" value="1" class="setbutton"><img src="stationlist.svg" width="30" height="30"></button>
 <button type="submit" name="settings" value="1" class="setbutton"><img src="settings.svg" width="30" height="30"></button>
 </form>
</head>

<body bgcolor="#1D519D" lang=EN-US style='tab-interval:.5in'>

<div>

<p>
<img width=225 height=225 src="PandoraP.ico" align=left hspace=12>
<span style='font-size:16.0pt;color:white'>________________________________</span></p>
<p><b><span style='font-size:30.0pt;color:white'>Stanley Solutions</span></b></p>
<p style='margin-bottom:0in;margin-bottom:.0001pt;line-height:normal'>
<b><span style='font-size:30.0pt;color:white'>Pandora Manager</span></b></p>
<span style='font-size:16.0pt;color:white'>________________________________</span></b></p>
<p><b><span style='font-size:16.0pt;color:white'>Now Playing: {{ songinfo }}</span></b></p>

<form align="center" method="post">
<p>
<button type="submit" name="playpause" value="1" class="button"><img src="play.svg" width="50" height="50"></button>
<button type="submit" name="playpause" value="1" class="button"><img src="pause.svg" width="50" height="50"></button>
<button type="submit" name="skip" value="1" class="button"><img src="skip.svg" width="50" height="50"></button>
</p>
<p>
<button type="submit" name="thumb_down" value="1" class="button"><img src="thumb_down.svg" width="50" height="50"></button>
<button type="submit" name="thumb_up" value="1" class="button"><img src="thumb_up.svg" width="50" height="50"></button>
</p>
<p>
<input type="submit" name="tired" class="button" value="Shelve Song">
</p>
</form>

</div>
</body>
<footer align="right">
  <p style='color:white'>&copy; Stanley Solutions</p>
  <p  style='color:white'>Contact information:
  <a style='color:#79CCF7' href="mailto:engineerjoe440@yahoo.com">engineerjoe440@yahoo.com</a></p>
</footer>
</html>
