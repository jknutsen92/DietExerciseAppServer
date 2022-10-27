function getFoodSnapshotItemNode(foodSnapshot) {
    return app.domParser.parseFromString(
        `<li api="${foodSnapshot.id ?? ''}">
            <img src="${foodSnapshot.image_url}" alt="${foodSnapshot.name}">
            <h1>${foodSnapshot.name}</h1>
        </li>`
    ,"text/html").body.firstChild;
}

function getFoodDetailsModalContent(foodDetails) {
    return app.domParser.parseFromString(
        `<div class="modal-body">
            <div class="image-panel">
                <img src="${foodDetails.image_url}" alt="${foodDetails.name}">
                <label>${foodDetails.servingQty} ${foodDetails.servingUnit} per serving</label>
            </div>
            <div class="info-panel">
                <table>
                    <caption>Nutrients Per Serving</caption>
                    <tbody>
                        <tr>
                            <td class="macro">Calories</td>
                            <td class="value">${foodDetails.calories}<em>(kcal)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Carbohydrates</td>
                            <td class="value">${foodDetails.macros.carbohydrates}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Protein</td>
                            <td class="value">${foodDetails.macros.protein}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Total Fat</td>
                            <td class="value">${foodDetails.macros.total_fat}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Saturated Fat</td>
                            <td class="value">${foodDetails.macros.saturated_fat}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Sugars</td>
                            <td class="value">${foodDetails.macros.sugars}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Sodium</td>
                            <td class="value">${foodDetails.macros.sodium}<em>(mg)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Cholesterol</td>
                            <td class="value">${foodDetails.macros.cholesterol}<em>(mg)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Dietary Fiber</td>
                            <td class="value">${foodDetails.macros.dietary_fiber}<em>(g)</em></td>
                        </tr>
                        <tr>
                            <td class="macro">Potassium</td>
                            <td class="value">${foodDetails.macros.potassium}<em>(mg)</em></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>`
    ,"text/html").body.firstChild;
}