// TODO: Rename to underscores
class Macros {                  // Nutritionix              Measures
    constructor(                // /v2/natural/nutrients
        total_fat,              // nf_total_fat             (g)
        saturated_fat,          // nf_saturated_fat         (g)
        cholesterol,            // nf_cholesterol           (mg)
        sodium,                 // nf_sodium                (mg)
        carbohydrates,          // nf_total_carbohydrate    (g)
        dietary_fiber,          // nf_dietary_fiber         (g)
        sugars,                 // nf_sugars                (g)
        protein,                // nf_protein               (g)
        potassium               // nf_potassium             (mg)
    ) {
        this.total_fat=         total_fat       ?? 0.0;
        this.saturated_fat=     saturated_fat   ?? 0.0;
        this.cholesterol=       cholesterol     ?? 0.0;
        this.sodium=            sodium          ?? 0.0;
        this.carbohydrates=     carbohydrates   ?? 0.0;
        this.dietary_fiber=     dietary_fiber   ?? 0.0;
        this.sugars=            sugars          ?? 0.0;
        this.protein=           protein         ?? 0.0;
        this.potassium=         potassium       ?? 0.0;
    }
}


class FoodDetails {             // Nutritionix
    constructor(                // /v2/natural/nutrients and /v2/search/item
        name,                   // food_name
        calories,               // nf_calories
        serving_qty,            // serving_qty
        serving_unit,           // serving_unit
        serving_weight,         // serving_weight_grams
        macros,                 // Macros object
        image_url,              // photo.highres   
        time_consumed           // consumed_at           
    ) {
        this.name=              name;
        this.calories=          calories;
        this.serving_qty=       serving_qty;
        this.serving_unit=      serving_unit;
        this.serving_weight=    serving_weight;
        this.macros=            macros;
        this.image_url=         image_url;
        this.time_consumed=     time_consumed
    }
}


class FoodSnapshot {            // Nutritionix
    constructor(                // /v2/search/instant
        id,                     // food_name/nix_item_id
        name,                   // food_name
        image_url               // photo.thumb
    ) {
        this.id=                id;
        this.name=              name;
        this.image_url=         image_url;
    }
}


class FoodEntry {
    constructor(
        name,
        calories,
        num_servings,
        serving_qty,
        serving_unit,
        serving_weight,
        macros,
        image_url,
        time_eaten
    ) {
        this.name=              name;
        this.calories=          calories;
        this.num_servings=      num_servings;
        this.serving_qty=       serving_qty;
        this.serving_unit=      serving_unit;
        this.serving_weight=    serving_weight;
        this.macros=            macros;
        this.image_url=         image_url;
        this.time_eaten=        time_eaten;
    }
}

class ExerciseDetails {
    constructor(
        name,
        calories_per_hour,
        time_completed
    ) {
        this.name=              name;
        this.calories_per_hour= calories_per_hour;
        this.time_completed=    time_completed;
    }
}


class ExerciseEntry {
    constructor(
        name,
        calories_per_hour,
        time_completed,
        duration
    ) {
        this.name=              name;
        this.calories_per_hour= calories_per_hour;
        this.time_completed =   time_completed;
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