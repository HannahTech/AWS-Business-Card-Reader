"use strict";

const serverUrl = "http://127.0.0.1:8000";

const imageContainer = document.getElementById("imageContainer");
const tableContainer = document.getElementById("tableContainer");
const foundCardsContainer = document.getElementById("foundCardsContainer");

async function extract() {
  imageContainer.innerHTML = "";
  tableContainer.innerHTML = "";
  const file = document.getElementById("file").files[0];
  const converter = new Promise(function (resolve, reject) {
    const reader = new FileReader();
    reader.addEventListener("load", function () {
      const imageUrl = reader.result;

      const img = document.createElement("img");
      img.src = imageUrl;
      // img.style.maxWidth = "750px";

      imageContainer.appendChild(img);
    });

    reader.readAsDataURL(file);

    reader.onload = () =>
      resolve(reader.result.toString().replace(/^data:(.*,)?/, ""));
    reader.onerror = (error) => reject(error);
  });
  const encodedString = await converter;

  document.getElementById("file").value = "";

  const response = await fetch(serverUrl + "/extract", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ filebytes: encodedString }),
  });

  const data = (await response.json()).data;

  console.log(data);
  createTable(tableContainer, data);
}

const createTable = (parentElement, data) => {
  // create the table element
  const table = document.createElement("table");
  table.setAttribute("border", "1");

  // add table headers
  const headers = ["name", "phone", "email", "website", "address", "other"];

  let rows = 0;
  for (const item of headers) {
    const len = data[item].length;
    rows = rows > len ? rows : len;
  }

  const headerRow = document.createElement("tr");
  headers.forEach((headerText) => {
    const header = document.createElement("th");
    header.textContent = headerText;
    headerRow.appendChild(header);
  });
  table.appendChild(headerRow);

  // add table rows
  for (let i = 0; i < rows; i++) {
    const row = document.createElement("tr");

    // add cells to each row
    for (let j = 0; j < 6; j++) {
      const cell = document.createElement("td");
      const val = data[headers[j]][i];
      if (val) cell.innerHTML = val;

      cell.contentEditable = true;

      row.appendChild(cell);
    }

    table.appendChild(row);
  }

  // add table to the container element
  parentElement.appendChild(table);
};

const create = async () => {
  const data = {
    name: [],
    phone: [],
    email: [],
    website: [],
    address: [],
    other: [],
  };

  const table = document.getElementsByTagName("table")[0];

  if (!table) return;

  const rows = table.rows.length;
  const cols = table.rows[0].cells.length;

  for (let col = 0; col < cols; col++) {
    for (let row = 1; row < rows; row++) {
      const val = table.rows[row].cells[col].innerHTML;
      if (val) {
        data[table.rows[0].cells[col].innerHTML].push(val);
      }
    }
  }

  if (data.name.length !== 1) {
    alert("name column must have");
    return;
  }

  for (const item in data) {
    if (data[item].length === 0) {
      delete data[item];
    } else if (data[item].length === 1) {
      data[item] = data[item][0];
    }
  }

  const response = await fetch(serverUrl + "/create", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const status = (await response.json()).status;

  alert(`upload ${status ? "" : "un"}successful`);

  console.log(status);
};

const read = async (name) => {
  foundCardsContainer.innerHTML = "";

  const response = await fetch(
    serverUrl + "/read/" + encodeURIComponent(name),
    {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );

  const items = await response.json();

  if (!items.length) foundCardsContainer.innerHTML = "No Record Found";

  items.forEach((item) => {
    console.log("item", item);
    createTable(foundCardsContainer, item);
  });

  console.log(items);
};
