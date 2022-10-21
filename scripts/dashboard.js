app = {                                                                     // Singleton containing application objects
    apis: new ExternalAPIs(),
    e: {
        main: {
            e:                          document.querySelector("body > main"),
            modalDialog: {//TODO: Refactor modal dialog to be outside of main
                e:                      document.querySelector(".modal-dialog"),
                header:                 document.querySelector(".modal-dialog > .modal-header"),
                content:                document.querySelector(".modal-dialog > .modal-content"),
                footer:                 document.querySelector(".modal-dialog > .modal-footer")
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
    domParser: new DOMParser()
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

        // Set the focus/mouseover and blur/mouseout handlers for each snapshot item
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
    // Replace header content
    app.e.main.modalDialog.header.querySelector("h2").innerText = `Add ${foodDetails.name}?`;
    
    // Replace modal content 
    const modalContent = getFoodDetailsModalContent(foodDetails);
    app.e.main.modalDialog.content.replaceWith(modalContent);
    app.e.main.modalDialog.content = modalContent;

    app.e.main.modalDialog.e.style.display = "block";
}

function destroyFoodDetailsWindow(event) {
    const window = event.target;
}

function populateExerciseDetailsList(event) {
    const query = event.target.value;
    // Delete existing list items
    console.log(query);
    // Populate on-
}

function spawnFoodConfirmationDialog(event) {
    const foodDetails = event.target.querySelector(".details");
    // Spawn window
}

function confirmFoodSelection(event) {
    const servings = event.target.parentElement.querySelector("#textConfirmQty");
}

function spawnExerciseConfirmationDialog(event) {
    const exerciseDetails = event.target.querySelector(".details");
}

function confirmExerciseConfirmation(event) {
    const hours = event.target.parentElement.querySelector("#textConfirmQty");
}

window.addEventListener("load", (event) => {
    initNewItemMenu();
});

window.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        app.e.main.newItem.dropdownBox.style.display = "none";
        app.e.main.modalDialog.e.style.display = "none";
        document.activeElement.blur();
    }
});

app.e.main.newItem.btnAddFoodItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.main.newItem.textInput.addEventListener("input", populateFoodSnapshotList);
});

app.e.main.newItem.btnAddExerciseItem.addEventListener("click", (event) => {
    activateNewItemSearch();
    app.e.main.newItem.textInput.addEventListener("input", populateExerciseDetailsList);
});

app.e.main.newItem.btnCancelNewItem.addEventListener("click", (event) => {
    resetNewItemMenu();
    app.e.main.newItem.textInput.removeEventListener("input", populateFoodSnapshotList);
    app.e.main.newItem.textInput.removeEventListener("input", populateExerciseDetailsList);
    app.e.main.newItem.list.innerHTML = "";
    app.e.main.newItem.textInput.value = "";
});

app.e.main.newItem.menu.addEventListener("focusin", (event) => {
    if (app.e.main.newItem.list.firstChild) {
        app.e.main.newItem.dropdownBox.style.display = "block";
    }
});

app.e.main.newItem.dropdownBox.addEventListener("focusout", (event) => {
    app.e.main.newItem.dropdownBox.style.display = "none";
});

window.addEventListener("click", (event) => {
    if (!event.path.includes(app.e.main.newItem.menu)) {
        app.e.main.newItem.dropdownBox.style.display = "none";
    }
    if (!event.path.includes(app.e.main.modalDialog.e)) {
        app.e.main.modalDialog.e.style.display = "none";
    }
});