var inputElement = document.getElementById("consignors_name");
const options_list = document.getElementById("list_consignors"); 

function fetchVendorNames(){
  
  let query = inputElement.value;
  options_list.innerHTML = '';

  if (query != "") { 
    fetch('/search_consigner', {
      method: "POST",
      body: JSON.stringify({
        names: query,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    }).then((response) => response.json())
    
    .then((data) => {
      var datas = [];
      var datas = data;
      for (li of datas){
        let option = document.createElement("li");
        option.innerHTML = li;
        option.className = "list-item"
        option.setAttribute("onclick", "select('"+ li +"')")
        options_list.appendChild(option);
  }
  });
}

}

function select(para){
  inputElement.value = para;
  options_list.innerHTML = "";
}
// Attach event listener to the input element
inputElement.addEventListener("keyup", fetchVendorNames);
