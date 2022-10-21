/*
    Contains all of the macronutrient values for a dish
*/
class Macros {                  // Nutritionix              Measures
    constructor(                // /v2/natural/nutrients
        totalFat,               // nf_total_fat             (g)
        saturatedFat,           // nf_saturated_fat         (g)
        cholesterol,            // nf_cholesterol           (mg)
        sodium,                 // nf_sodium                (mg)
        carbohydrates,          // nf_total_carbohydrate    (g)
        dietaryFiber,           // nf_dietary_fiber         (g)
        sugars,                 // nf_sugars                (g)
        protein,                // nf_protein               (g)
        potassium               // nf_potassium             (mg)
    ) {
        this.totalFat =         totalFat        ?? 0.0;
        this.saturatedFat =     saturatedFat    ?? 0.0;
        this.cholesterol =      cholesterol     ?? 0.0;
        this.sodium =           sodium          ?? 0.0;
        this.carbohydrates =    carbohydrates   ?? 0.0;
        this.dietaryFiber =     dietaryFiber    ?? 0.0;
        this.sugars =           sugars          ?? 0.0;
        this.protein =          protein         ?? 0.0;
        this.potassium =        potassium       ?? 0.0;
    }
}

/*
    The detailed food data from the API
*/
class FoodDetails {             // Nutritionix
    constructor(                // /v2/natural/nutrients and /v2/search/item
        name,                   // food_name
        calories,               // nf_calories
        servingQty,             // serving_qty
        servingUnit,            // serving_unit
        servingWeight,          // serving_weight_grams
        macros,                 // Macros object
        imageURL,               // photo.highres   
        timeEaten               // consumed_at           
    ) {
        this.name =             name;
        this.calories =         calories;
        this.servingQty =       servingQty;
        this.servingUnit =      servingUnit;
        this.servingWeight =    servingWeight;
        this.macros =           macros;
        this.imageURL =         imageURL;
        this.timeEaten =        timeEaten
    }
}

/*
    Represents food data contained in a single list item produced by autocomplete search
*/
class FoodSnapshot {            // Nutritionix
    constructor(                // /v2/search/instant
        idInAPI,                // food_name/nix_item_id
        name,                   // food_name
        imageURL                // photo.thumb
    ) {
        this.idInAPI =          idInAPI;
        this.name =             name;
        this.imageURL =         imageURL;
    }
}

/*
    The macros and calories consumed in a single item to be sent to the server for storage in historical database
*/
class FoodConsumed {
    constructor(
        name,
        calories,
        numServings,
        servingQty,
        servingUnit,
        servingWeight,
        macros,
        imageURL
    ) {
        this.name =             name;
        this.calories =         calories;
        this.numServings =      numServings;
        this.servingQty =       servingQty;
        this.servingUnit =      servingUnit;
        this.servingWeight =    servingWeight;
        this.macros =           macros;
        this.imageURL =         imageURL;
    }
}

class ExerciseDetails {
    constructor(
        name,                   // name
        caloriesPerHour,
        timeCompleted
    ) {
        this.name =             name;
        this.caloriesPerHour =  caloriesPerHour;
        this.timeCompleted =    timeCompleted;
    }
}

class ExerciseCompleted {
    constructor(
        name,
        caloriesPerHour,
        timeCompleted,
        duration
    ) {
        this.name =             name;
        this.caloriesPerHour =  caloriesPerHour;
        this.timeCompleted =    timeCompleted;
        this.duration =         duration;
    }
}

class UserDetails {
    constructor(
        gender,
        weight,
        height,
        age
    ) {
        this.gender =           gender;
        this.weight =           weight;
        this.height =           height;
        this.age =              age;
    }
}