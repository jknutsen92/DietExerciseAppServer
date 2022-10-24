app = {                                                                     // Singleton containing application objects
    apis: new ExternalAPIs(),
    e: {
        main: {
            e:                          document.querySelector("body > main"),
            modalDialog: {//TODO: Refactor modal dialog to be outside of main
                background:             document.querySelector(".modal-background"),
                content:                document.querySelector(".modal-background > .modal-content"),
                header:                 document.querySelector(".modal-content > .modal-header"),
                close:                  document.querySelector(".modal-content > .modal-header > .close"),
                body:                   document.querySelector(".modal-content > .modal-body"),
                footer:                 document.querySelector(".modal-content > .modal-footer"),
                inputQty:               document.querySelector("#modalInputQty"),
                btnConfirm:             document.querySelector("#btnModalConfirm")           
            },
            newItem: {//TODO: Refactor new item menu to be outside of main
                btnAddFoodItem:         document.querySelector("#btnAddFoodItem"),
                btnAddExerciseItem:     document.querySelector("#btnAddExerciseItem"),
                btnCancelNewItem:       document.querySelector("#btnCancelNewItem"),  
                dropdownBox:            document.querySelector(".dropdown-menu > .dropdown-box"),
                dropdownMenu:           document.querySelector(".dropdown-menu"),
                list:                   document.querySelector("#ulItemList"),
                menu:                   document.querySelector("div.new-item-menu"),
                selectPanel:            document.querySelector(".new-item-menu > .select-panel"),
                submitPanel:            document.querySelector(".new-item-menu > .submit-panel"),
                textInput:              document.querySelector("#textItemSearch")
            }
        }
    },
    domParser: new DOMParser(),
    uiState: {
        modalDialog: {
            selectedFoodDetails: null
        }
    }
};

function initNewItemMenu() {
    const mainWidth = parseFloat(app.e.main.e.getBoundingClientRect().width);
    app.e.main.newItem.textInput.setAttribute("size", (mainWidth * 0.08));
}

function resetNewItemMenu() {
    app.e.main.newItem.selectPanel.style.display = "block";
    app.e.main.newItem.textInput.style.display =   "none";
    app.e.main.newItem.dropdownBox.style.display = "none";
    app.e.main.newItem.submitPanel.style.display = "none";

    app.e.main.newItem.textInput.removeEventListener("input", populateFoodSnapshotList);
    app.e.main.newItem.textInput.removeEventListener("input", populateExerciseDetailsList);
    app.e.main.newItem.list.innerHTML = "";
    app.e.main.newItem.textInput.value = "";
}

function activateNewItemSearch() {
    app.e.main.newItem.selectPanel.style.display = "none";
    app.e.main.newItem.textInput.style.display =   "inline";
    app.e.main.newItem.submitPanel.style.display = "block";
}

async function populateFoodSnapshotList(event) {
    const query =       event.target.value;

    // Delete existing list items
    app.e.main.newItem.list.innerHTML = "";

    // Show dropdown box
    // TODO: Animate this so that it smoothly drops into position
    app.e.main.newItem.dropdownBox.style.display = "block";

    // Populate with food snapshots
    const snapshots = await app.apis.food.search(query);
    for (const snapshot of snapshots) {
        // Create item element with snapshot data
        const item = getFoodSnapshotItemNode(snapshot);

        // Set the handlers for each snapshot item
        item.addEventListener("click", spawnFoodDetailsWindow);

        // Insert item element into list
        app.e.main.newItem.list.appendChild(item);
    }
}

async function spawnFoodDetailsWindow(event) {
    const snapshotListItem = event.target;
    // Get the food details and render a popup window
    const response = await app.apis.food.getFood(
        new FoodSnapshot(
            snapshotListItem.getAttribute("idinapi"),
            snapshotListItem.querySelector("h1").innerText,
            null
        )
    );
    const foodDetails = response[0];
    app.uiState.modalDialog.selectedFoodDetails = foodDetails;

    // Replace header content
    app.e.main.modalDialog.header.querySelector("h2 > span").innerText = foodDetails.name;
    
    // Replace modal content 
    const modalContent = getFoodDetailsModalContent(foodDetails);
    app.e.main.modalDialog.body.replaceWith(modalContent);
    app.e.main.modalDialog.body = modalContent;

    // Set handlers
    app.e.main.modalDialog.inputQty.addEventListener("keydown", confirmFoodSelection);
    app.e.main.modalDialog.btnConfirm.addEventListener("click", confirmFoodSelection);
    
    // Display modal dialog
    app.e.main.modalDialog.background.style.display = "block";
}

function confirmFoodSelection(event) {
    const servings = parseFloat(app.e.main.modalDialog.inputQty.value);
    const details = app.uiState.modalDialog.selectedFoodDetails;
    const foodConsumed = new FoodConsumed(
        details.name,
        details.calories,
        servings,
        details.servingQty,
        details.servingUnit,
        details.servingWeight,
        details.macros,
        details.imageURL
    )

    // TODO: Send FoodConsumed to server
    

    resetModalDialog();
    resetNewItemMenu();
    insertFoodSelectionIntoUI(foodConsumed);
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
    const servings = parseFloat(app.e.main.modalDialog.inputQty.value);
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

function resetModalDialog() {
    //TODO:
    // Unset handlers
    // Hide food details dialog
}

window.addEventListener("load", (event) => {
    initNewItemMenu();
});

window.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        app.e.main.newItem.dropdownBox.style.display = "none";
        app.e.main.modalDialog.background.style.display = "none";
        document.activeElement.blur();
    }
});

// 'Add Food' button listeners
app.e.main.newItem.btnAddFoodItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.main.newItem.textInput.addEventListener("input", populateFoodSnapshotList);
});

// 'Add Exercise' button listeners
app.e.main.newItem.btnAddExerciseItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.main.newItem.textInput.addEventListener("input", populateExerciseDetailsList);
});

// New item cancel button listeners
app.e.main.newItem.btnCancelNewItem.addEventListener("click", resetNewItemMenu);

// New item menu listeners
app.e.main.newItem.menu.addEventListener("focusin", (event) => {
    if (app.e.main.newItem.list.firstChild) {
        app.e.main.newItem.dropdownBox.style.display = "block";
    }
});

// New item dropdown box listeners
app.e.main.newItem.dropdownBox.addEventListener("focusout", (event) => {
    app.e.main.newItem.dropdownBox.style.display = "none";
});

// General window click listener
window.addEventListener("click", (event) => {
    if (!event.path.includes(app.e.main.newItem.menu)) {
        app.e.main.newItem.dropdownBox.style.display = "none";
    }
    if (event.target == app.e.main.modalDialog.background) {
        app.e.main.modalDialog.background.style.display = "none";
    }
});

// Modal dialog window close button listener
app.e.main.modalDialog.close.addEventListener("click", (event) => {
    app.e.main.modalDialog.background.style.display = "none";
});