class FoodAPI {
    #id
    #key

    constructor(id, key) {
        this.#id = id;
        this.#key = key;
    }

    async search(query) {
        const response = await fetch(`https://trackapi.nutritionix.com/v2/search/instant?query=${query}`, {
            method: "GET",
            headers: {
                "x-app-id": this.#id,
                "x-app-key": this.#key
            }
        });
        try {
            const data = await response.json();
            const snapshots = [];
            for (const branded of data.branded) {
                snapshots.push(new FoodSnapshot(
                    branded.nix_item_id,
                    branded.brand_name_item_name,
                    branded.photo.thumb
                ));
            }
            for (const common of data.common) {
                snapshots.push(new FoodSnapshot(
                    null,
                    common.food_name,
                    common.photo.thumb
                ));
            }
            // TODO: Sort by relevance instead of alphabetically
            return snapshots.sort((a, b) => a.name.localeCompare(b.name));
        }
        catch (error) {
            console.error(`Error: ${error}`);
        }
    }

    async getFood(foodSnapshot) {
        // TODO: refactor
        if (!foodSnapshot.idInAPI) {
            return await this.#getNatural(foodSnapshot.name);
        }
        else {
            return await this.#getItem(foodSnapshot.idInAPI);
        }
    }

    async #getItem(id) {
        const response = await fetch(`https://trackapi.nutritionix.com/v2/search/item?nix_item_id=${id}`, {
            method: "GET",
            headers: {
                "x-app-id": this.#id,
                "x-app-key": this.#key
            }
        });
        try {
            const data = await response.json();
            const details = [];
            for (const food of data.foods) {
                details.push(new FoodDetails(
                    food.food_name,
                    food.nf_calories,
                    food.serving_qty,
                    food.serving_unit,
                    food.serving_weight_grams,
                    new Macros(
                        food.nf_total_fat,
                        food.nf_saturated_fat,
                        food.nf_cholesterol,
                        food.nf_sodium,
                        food.nf_total_carbohydrate,
                        food.nf_dietary_fiber,
                        food.nf_sugars,
                        food.nf_protein,
                        food.nf_potassium
                    ),
                    food.photo.highres ?? food.photo.thumb,
                    new Date().toUTCString()
                ));
            }
            return details;
        }
        catch (error) {
            console.error(`Error: ${error}`);
        }
    }

    async #getNatural(name) {
        const response = await fetch("https://trackapi.nutritionix.com/v2/natural/nutrients", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-app-id": this.#id,
                    "x-app-key": this.#key
                },
                body: JSON.stringify({
                    "query": name
                })
        });
        try {
            const data = await response.json();
            const details = [];
            for (const food of data.foods) {
                details.push(new FoodDetails(
                    food.food_name,
                    food.nf_calories,
                    food.serving_qty,
                    food.serving_unit,
                    food.serving_weight_grams,
                    new Macros(
                        food.nf_total_fat,
                        food.nf_saturated_fat,
                        food.nf_cholesterol,
                        food.nf_sodium,
                        food.nf_total_carbohydrate,
                        food.nf_dietary_fiber,
                        food.nf_sugars,
                        food.nf_protein,
                        food.nf_potassium
                    ),
                    food.photo.highres ?? food.photo.thumb,
                    new Date().toUTCString()
                ));
            }
            return details;
        }
        catch (error) {
            console.error(`Error: ${error}`);
        }
    }
}

class ExerciseAPI {
    #id
    #key

    constructor(id, key, userDetails) {
        this.#id = id;
        this.#key = key;
        this.userDetails = userDetails
    }

    async getExercise(query) {
        const response = await fetch("https://trackapi.nutritionix.com/v2/natural/exercise", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-app-id": this.#id,
                "x-app-key": this.#key
            },
            body: JSON.stringify({
                "query": query,
                "gender": this.userDetails.gender,
                "weight_kg": this.userDetails.weight,
                "height_cm": this.userDetails.height,
                "age": this.userDetails.age
            })
        });
        try {
            const data = await response.json();
            const details = [];
            for (const exercise of data.exercises) {
                const durationHours = 60.0 / parseFloat(exercise.duration_min);
                const cals = parseFloat(exercise.nf_calories);
                details.push(new ExerciseDetails(
                    exercise.name,
                    cals * durationHours,
                    new Date().toUTCString()
                ));
            }
            return details;
        }
        catch (error) {
            console.error(`Error: ${error}`);
        }
    }
}

class ExternalAPIs {
    constructor() {
        const foodId =      document.querySelector("meta[name='food_api_id']").getAttribute("content");
        const foodKey =     document.querySelector("meta[name='food_api_key']").getAttribute("content");
        const exerciseId =  document.querySelector("meta[name='exercise_api_id']").getAttribute("content");
        const exerciseKey = document.querySelector("meta[name='exercise_api_key']").getAttribute("content");
        const userGender =  document.querySelector("meta[name='user_gender']").getAttribute("content");
        const userWeight =  document.querySelector("meta[name='user_weight']").getAttribute("content");
        const userHeight =  document.querySelector("meta[name='user_height']").getAttribute("content");
        const userAge =     document.querySelector("meta[name='user_age']").getAttribute("content");
        
        return {
            food: new FoodAPI(
                foodId,
                foodKey
            ),
            exercise: new ExerciseAPI(
                exerciseId,
                exerciseKey,
                new UserDetails(
                    userGender,
                    userWeight,
                    userHeight,
                    userAge
                )
            )
        };
    }
}