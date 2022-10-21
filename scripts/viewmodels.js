function getFoodSnapshotItemNode(foodSnapshot) {
    return app.domParser.parseFromString(
        `<li idInAPI="${foodSnapshot.idInAPI ?? ''}">
            <img src="${foodSnapshot.imageURL}" alt="${foodSnapshot.name}">
            <h1>${foodSnapshot.name}</h1>
        </li>`
    ,"text/html").body.firstChild;
}

function getFoodDetailsModalContent(foodDetails) {
    return app.domParser.parseFromString(
        `<div class="modal-content">
            <div>
                <img src="${foodDetails.imageURL}" alt="${foodDetails.name}">
                <label>${foodDetails.servingQty} ${foodDetails.servingUnit} per serving</label>
            </div>
            <div>
                <table>
                    <caption>Nutrients Per Serving</caption>
                    <thead>
                        <tr>
                            <th>Macro</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Calories</td>
                            <td>${foodDetails.calories}<em>(kcal)</em></td>
                        </tr>
                        <tr>
                            <td>Carbohydrates</td>
                            <td>${foodDetails.macros.carbohydrates}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Protein</td>
                            <td>${foodDetails.macros.protein}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Total Fat</td>
                            <td>${foodDetails.macros.totalFat}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Saturated Fat</td>
                            <td>${foodDetails.macros.saturatedFat}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Sugars</td>
                            <td>${foodDetails.macros.sugars}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Sodium</td>
                            <td>${foodDetails.macros.sodium}<em>(mg)</em></td>
                        </tr>
                        <tr>
                            <td>Cholesterol</td>
                            <td>${foodDetails.macros.cholesterol}<em>(mg)</em></td>
                        </tr>
                        <tr>
                            <td>Dietary Fiber</td>
                            <td>${foodDetails.macros.dietaryFiber}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td>Potassium</td>
                            <td>${foodDetails.macros.potassium}<em>(mg)</em></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>`
    ,"text/html").body.firstChild;
}