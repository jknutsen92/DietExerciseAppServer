// Singleton containing application objects
app = {
    apis: new ExternalAPIs(),
    e: {
        header: {
            e:                      document.querySelector("header"),
            newItem: {
                btnAddFoodItem:     document.querySelector("#btnAddFoodItem"),
                btnAddExerciseItem: document.querySelector("#btnAddExerciseItem"),
                btnCancelNewItem:   document.querySelector("#btnCancelNewItem"),  
                dropdownBox:        document.querySelector(".dropdown-menu > .dropdown-box"),
                dropdownMenu:       document.querySelector(".dropdown-menu"),
                list:               document.querySelector("#ulItemList"),
                menu:               document.querySelector("div.new-item-menu"),
                selectPanel:        document.querySelector(".new-item-menu > .select-panel"),
                submitPanel:        document.querySelector(".new-item-menu > .submit-panel"),
                textInput:          document.querySelector("#textItemSearch")
            }
        },
        main: {
            e:                      document.querySelector("body > main"),
        },
        modalDialog: {
            background:             document.querySelector(".modal-background"),
            content:                document.querySelector(".modal-background > .modal-content"),
            header:                 document.querySelector(".modal-content > .modal-header"),
            close:                  document.querySelector(".modal-content > .modal-header > .close"),
            body:                   document.querySelector(".modal-content > .modal-body"),
            footer:                 document.querySelector(".modal-content > .modal-footer"),
            inputQty:               document.querySelector("#modalInputQty"),
            btnConfirm:             document.querySelector("#btnModalConfirm")           
        }
    },
    domParser: new DOMParser(),
    uiState: {
        modalDialog: {
            selectedFoodDetails: null
        }
    }
};

// UI controllers
function initNewItemMenu() {
    const mainWidth = parseFloat(app.e.main.e.getBoundingClientRect().width);
    app.e.header.newItem.textInput.setAttribute("size", (mainWidth * 0.08));
}

function resetNewItemMenu() {
    app.e.header.newItem.selectPanel.style.display = "block";
    app.e.header.newItem.textInput.style.display =   "none";
    app.e.header.newItem.dropdownBox.style.display = "none";
    app.e.header.newItem.submitPanel.style.display = "none";

    app.e.header.newItem.textInput.removeEventListener("input", populateFoodSnapshotList);
    app.e.header.newItem.textInput.removeEventListener("input", populateExerciseDetailsList);
    app.e.header.newItem.list.innerHTML = "";
    app.e.header.newItem.textInput.value = "";
}

function activateNewItemSearch() {
    app.e.header.newItem.selectPanel.style.display = "none";
    app.e.header.newItem.textInput.style.display =   "inline";
    app.e.header.newItem.submitPanel.style.display = "block";
}

function resetModalDialog() {
    //TODO:
    // Unset handlers
    // Hide food details dialog
}

// External API data UI population controllers
async function populateFoodSnapshotList(event) {
    const query =       event.target.value;

    // Delete existing list items
    app.e.header.newItem.list.innerHTML = "";

    // Show dropdown box
    // TODO: Animate this so that it smoothly drops into position
    app.e.header.newItem.dropdownBox.style.display = "block";

    // Populate with food snapshots
    const snapshots = await app.apis.food.search(query);
    for (const snapshot of snapshots) {
        // Create item element with snapshot data
        const item = getFoodSnapshotItemNode(snapshot);

        // Set the handlers for each snapshot item
        item.addEventListener("click", spawnFoodDetailsWindow);

        // Insert item element into list
        app.e.header.newItem.list.appendChild(item);
    }
}

async function spawnFoodDetailsWindow(event) {
    const snapshotListItem = event.target;
    // Get the food details and render a popup window
    const response = await app.apis.food.getFood(
        new FoodSnapshot(
            snapshotListItem.getAttribute("api"),
            snapshotListItem.querySelector("h1").innerText,
            null
        )
    );
    const foodDetails = response[0];
    app.uiState.modalDialog.selectedFoodDetails = foodDetails;

    // Replace header content
    app.e.modalDialog.header.querySelector("h2 > span").innerText = foodDetails.name;
    
    // Replace modal content 
    const modalContent = getFoodDetailsModalContent(foodDetails);
    app.e.modalDialog.body.replaceWith(modalContent);
    app.e.modalDialog.body = modalContent;

    // Set handlers
    app.e.modalDialog.inputQty.addEventListener("keydown", confirmFoodSelection);
    app.e.modalDialog.btnConfirm.addEventListener("click", confirmFoodSelection);
    
    // Display modal dialog
    app.e.modalDialog.background.style.display = "block";
}

function confirmFoodSelection(event) {
    const servings = parseFloat(app.e.modalDialog.inputQty.value);
    const details = app.uiState.modalDialog.selectedFoodDetails;
    const foodEntry = new FoodEntry(
        details.name,
        details.calories,
        servings,
        details.serving_qty,
        details.serving_unit,
        details.serving_weight,
        details.macros,
        details.image_url,
        details.time_consumed
    )

    // TODO: Send FoodEntry to server
    console.log("Sending to the server: ", foodEntry);

    resetModalDialog();
    resetNewItemMenu();
    insertFoodSelectionIntoUI(foodEntry);
    app.uiState.modalDialog.selectedFoodDetails = null;
}

function insertFoodSelectionIntoUI(foodConsumed) {
    // TODO:
    // Insert item into ui controls

    // Update dynamic UI
}

function populateExerciseDetailsList(event) {
    const query = event.target.value;
    //TODO:
    // Get exercise details

    // Set handlers

    // Insert into list
}

async function spawnExerciseDetailsWindow(event) {
    //TODO:
}

function confirmExerciseSelection(event) {
    const servings = parseFloat(app.e.modalDialog.inputQty.value);
    resetModalDialog()
    resetNewItemMenu()
    //TODO:
    // Hide food details dialog
    // Reset food snapshot list
    // Insert into UI tables/graphs/etc
}

function insertExerciseSelectionIntoUI(foodDetails) {
    //TODO:
    // Insert item into ui controls

    // Update dynamic UI
}

window.addEventListener("load", (event) => {
    initNewItemMenu();
});

window.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        app.e.header.newItem.dropdownBox.style.display = "none";
        app.e.modalDialog.background.style.display = "none";
        document.activeElement.blur();
    }
});

// 'Add Food' button listeners
app.e.header.newItem.btnAddFoodItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.header.newItem.textInput.addEventListener("input", populateFoodSnapshotList);
});

// 'Add Exercise' button listeners
app.e.header.newItem.btnAddExerciseItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.header.newItem.textInput.addEventListener("input", populateExerciseDetailsList);
});

// New item cancel button listeners
app.e.header.newItem.btnCancelNewItem.addEventListener("click", resetNewItemMenu);

// New item menu listeners
app.e.header.newItem.menu.addEventListener("focusin", (event) => {
    if (app.e.header.newItem.list.firstChild) {
        app.e.header.newItem.dropdownBox.style.display = "block";
    }
});

// New item dropdown box listeners
app.e.header.newItem.dropdownBox.addEventListener("focusout", (event) => {
    app.e.header.newItem.dropdownBox.style.display = "none";
});

// General window click listener
window.addEventListener("click", (event) => {
    if (!event.path.includes(app.e.header.newItem.menu)) {
        app.e.header.newItem.dropdownBox.style.display = "none";
    }
    if (event.target == app.e.modalDialog.background) {
        app.e.modalDialog.background.style.display = "none";
    }
});

// Modal dialog window close button listener
app.e.modalDialog.close.addEventListener("click", (event) => {
    app.e.modalDialog.background.style.display = "none";
});