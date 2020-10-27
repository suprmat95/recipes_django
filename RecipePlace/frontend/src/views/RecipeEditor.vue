<template lang="html">
    <div class="container">
        <br/>
        <h1 class="mb-3">Aggiungi una Ricetta</h1>
        <h3 class="mb-3 align-left">Titolo</h3>

        <div class="row">
            <div class="col-12">
                <md-field>
                    <label>Aggiugingi il titolo della ricetta</label>
                    <md-input v-model="recipeBody"></md-input>
                </md-field>
                <br/>
            </div>
        </div>
        <br/>
        <hr/>
        <h3 class="mb-3 align-left">Descrizione della ricetta</h3>

        <div class="row">
            <div class="col-12">
                <md-field>
                    <label>Aggiungi la descrizione Ricetta</label>
                    <md-input v-model="recipeDescription"></md-input>
                </md-field>
                <br/>
            </div>
        </div>
        <br/>
        <hr/>
        <h3 class="mb-3 align-left">Durata Preparazione della ricetta</h3>
        <md-field>
            <label>Minuti</label>
            <md-input type="number" id="snackbar-duration" v-model="time_to_prepare" ></md-input>
        </md-field>
         <br/>
        <hr/>
        <h3 class="mb-3 align-left">Numero di persone</h3>
        <md-field>
            <label>Aggiungi numero persone</label>
            <md-input type="number" id="snackbar-duration" v-model="people" ></md-input>
        </md-field>
        <br/>
        <hr/>
        <h3 class="mb-3 align-left">Foto</h3>
        <div class="row">
            <div class="col-12">
                <picture-input
                        @change="onChange($event)"
                        class="align-left"
                        name="picture"
                        ref="file"
                        width="200"
                        height="200"
                        margin="16"
                        accept="image/jpeg,image/png, image/png"
                        size="5"
                        buttonClass="btn"
                        :prefill="previousPicture"
                        :customStrings="{
            upload: '<h1>RECIPEEE!</h1>',
            drag: 'Drag a GIF 🍝'
          }"
                >
                </picture-input>
            </div>
        </div>
        <br/>
        <br/>
        <hr/>

        <h3 class="mb-3 align-left">Ingredienti</h3>
        <md-button
                class="md-icon-button md-raised align-left"
                @click="addRowIngredient"
        >
            <md-icon>add</md-icon>
        </md-button>
        <li v-for="(ingredient, index) in ingredients" :key="index">
            <div class="row">
                <div class="col-12">
                    <md-field class="form-control-ing-name">
                        <label>Nome ingrediente</label>
                        <md-input v-model="ingredient.name"></md-input>
                    </md-field>
                    <md-field class="form-control-ing-quantity">
                        <label>Quantità</label>
                        <md-input v-model="ingredient.quantity"></md-input>
                    </md-field>

                    <md-field class="md-layout-item">
                        <label>Unità</label>
                        <md-select v-model="ingredient.unity" name="unity" id="unity">
                            <md-option value="Grammi">Grammi</md-option>
                            <md-option value="Litri">Litri</md-option>
                            <md-option value="Unità">Unità</md-option>

                        </md-select>
                    </md-field>
                    <br/>
                    <md-button
                            class="md-icon-button md-raised align-left child"
                            @click="deleteRowIngredient(index)"
                    >
                        <md-icon> delete</md-icon>
                    </md-button>
                </div>
            </div>
        </li>
        <br/>
        <hr/>
        <h3 class="mb-3 align-left">Passaggi</h3>
        <md-button
                class="md-icon-button md-raised align-left"
                @click="addRowPassage"
        >
            <md-icon>add</md-icon>
        </md-button>

        <li v-for="(input, index) in inputs" :key="'A' + index">
            <div class="row">
                <div class="col-12">
                    <!--   <form action="http://localhost:8000/api/questions/" -->
                    <md-field class="form-passage">
                        <label>Aggiungi la spiegazione del passaggio</label>
                        <md-input v-model="input.body"></md-input>
                    </md-field>
                    <md-button
                            class="md-icon-button md-raised "
                            @click="deleteRowPassage(index)"
                    >
                        <md-icon> delete</md-icon>
                    </md-button>
                </div>
            </div>

            <br/>
            <div class="hello">
                <picture-input
                        @change="handleFileChange($event, index)"
                        class="align-left"
                        name="picture"
                        ref="file"
                        width="150"
                        height="150"
                        margin="16"
                        accept="image/jpeg,image/png,image/gif"
                        size="5"
                        buttonClass="btn"
                        :prefill="input.picture"
                        :customStrings="{
            upload: '<h1>RECIPEEE!</h1>',
            drag: 'Drag a GIF 🍝'
          }"
                >
                </picture-input>
            </div>
        </li>

        <br/>
        <br/>
        <div class="row">
            <div class="col-12">
                <md-button class="md-raised md-primary align-left" @click="onSubmit">
                    UPLOAD
                </md-button>
            </div>
        </div>
        <p class="muted error mt-2">{{ error }}</p>
    </div>
</template>

<script>
    import {apiService} from "../common/api.service";
    import PictureInput from "vue-picture-input";
    import {CSRF_TOKEN} from "../common/csrf_token.js";
    import axios from "axios";

    export default {
        name: "RecipeEditor",
        components: {
            PictureInput
        },
        props: {
            slug: {
                type: String,
                error: null
            },
            previousRecipe: {
                type: String,
                required: false
            },
            previousPicture: {
                type: String,
                required: false
            },
            token: {
                type: String,
                required: true
            },
            previousInputs: {
                type: Array,
                required: false
            },
            previousIngredients: {
                type: Array,
                required: false
            },
            previousRecipeDescription: {
                type: String,
                required: false
            },
        },
        data() {
            return {
                recipeBody: this.previousRecipe || null,
                recipeDescription: this.previousRecipeDescription || null,
                time_to_prepare: null,
                people: null,
                inputs: [],
                ingredients: [],
                error: null,
                picture: null
            };
        },

        async beforeRouteEnter(to, from, next) {
            to.params.token = CSRF_TOKEN;
            if (to.params.slug !== undefined) {
                let endpoint = `/api/recipes/${to.params.slug}/`;
                await apiService(endpoint).then(data => {
                    to.params.previousRecipe = data.content;
                    to.params.previousPicture = data.picture;
                    to.params.previousInputs = data.passage;
                    to.params.previousIngredients = data.ingredient;
                });
            }
            return next();
        },
        methods: {
            dataURLtoFile(dataurl, filename) {
                var arr = dataurl.split(","),
                    mime = arr[0].match(/:(.*?);/)[1],
                    bstr = atob(arr[1]),
                    n = bstr.length,
                    u8arr = new Uint8Array(n);
                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n);
                }

                return new File([u8arr], filename, {type: mime});
            },
            addRowPassage() {
                this.inputs.push({
                    body: "",
                    picture: null
                });
            },
            addRowIngredient() {
                this.ingredients.push({
                    name: "",
                    quantity: null,
                    unity: ""
                });
            },
            deleteRowPassage(index) {
                this.inputs.splice(index, 1);
            },
            deleteRowIngredient(index) {
                this.ingredients.splice(index, 1);
            },
            handleFileChange(event, index) {
                console.log("New picture selected!");
                if (event) {
                    console.log("Picture loaded.");
                    this.inputs[index].picture = this.dataURLtoFile(
                        event,
                        this.recipeBody + "-picture.jpg"
                    );
                    console.log(this.inputs[index].picture);
                } else {
                    console.log("FileReader API not supported: use the <form>, Luke!");
                }
            },
            onChange(event) {
                console.log("New picture selected!");
                if (event) {
                    this.picture = this.dataURLtoFile(
                        event,
                        this.recipeBody + "-picture.jpg"
                    );
                    console.log(this.picture);
                } else {
                    console.log("FileReader API not supported: use the <form>, Luke!");
                }
            },
            onSubmit() {
                const headers = {"X-CSRFTOKEN": CSRF_TOKEN};
                const fd = new FormData();
                fd.append("content", this.recipeBody);
                fd.append("description", this.recipeDescription);
                fd.append("picture", this.picture, this.picture.name);
                fd.append("time_to_prepare", this.time_to_prepare);
                fd.append("people", this.people);
                const endpoint = "http://localhost:8000/api/recipes/";
                axios
                    .post(endpoint, fd, {headers: headers})
                    .then(recipe_data => {
                        console.log(recipe_data.data.slug);
                        this.inputs.forEach(input => {
                            const fp = new FormData();
                            fp.append("body", input.body);
                            fp.append("picture", input.picture);
                            axios
                                .post(endpoint + recipe_data.data.slug + "/passage/", fp, {
                                    headers: headers
                                })
                                .then(res => {
                                    console.log("recipes res");
                                    console.log(res);

                                });
                        });
                        this.ingredients.forEach(ingredient => {
                            const fi = new FormData();
                            fi.append("name", ingredient.name);
                            fi.append("quantity", ingredient.quantity);
                            fi.append("unity", ingredient.unity);
                            axios
                                .post(endpoint + recipe_data.data.slug + "/ingredient/", fi, {
                                    headers: headers
                                })
                                .then(res => {
                                    console.log("recipes ingredients");
                                    console.log(res);
                                });
                        });

                        this.$router.push({
                            name: "home",
                        });
                    })
                    .catch(err => console.log(err));
            }

        },
        created() {
            document.title = "Editor - RecipePlace";
            console.log("created");

            if (
                this.previousIngredients !== undefined &&
                this.previousIngredients.length > 0
            ) {
                this.ingredients = this.previousIngredients;
            } else {
                this.ingredients.push({
                    name: "",
                    quantity: "",
                    unity: ""
                });
            }
            if (this.previousInputs !== undefined && this.previousInputs.length > 0) {
                this.inputs = this.previousInputs;
            } else {
                this.inputs.push({
                    body: "",
                    image: null
                });
            }
        }
    };
</script>

<style scoped>
    .form-control {
        width: 60%;
        float: left;
    }

    .row {
        width: 100%;
    }

    .align-right {
        float: right;
    }

    .hello {
        width: 50%;
        float: left;
    }

    .align-left {
        float: left;
        margin: 10px;
    }

    .form-control-ing-name {
        float: left;
        width: 30%;
        margin: 10px;
        height: 45px;
    }

    .form-control-ing-quantity {
        float: left;
        width: 15%;
        height: 45px;
        margin: 10px;
    }

    .md-layout-item {
        float: left;
        width: 10%;
        margin: 10px;
    }

    .form-passage {
        float: left;
        width: 80%;
    }
</style>
