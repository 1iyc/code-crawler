var cl = document.getElementById("sokresult").getElementsByTagName("a")
var el = document.getElementById("tab1").getElementsByTagName("td")
var text = ''
var hscode = document.getElementById("hscommnet").getElementsByTagName("b")[0].innerText.slice(3)
for (e in el) {
	 if (el[e].innerText == undefined) {
		   break;
		  }
	 text += hscode + ", " + el[e].innerText + "\n"
}
console.log(text)
cl[++i].click()
