<template lang="html">
    <div class="container">
        <h1 class="mb-3">Aggiungi una Ricetta</h1>
        <h3 class="mb-3 align-left">Aggiungi il titolo</h3>

        <div class="row">
            <div class="col-12">
                <!--   <form action="http://localhost:8000/api/questions/"
                          method="post"
                          encType="multipart/form-data"
                        > -->

                <textarea
                        name="content"
                        v-model="questionBody"
                        class="form-control"
                        placeholder="Aggiungi titolo alla ricetta?"
                        rows="1"
                ></textarea>

                <div class="hello align-right">

                </div>
                <br/>
            </div>
        </div>
        <br/>
        <h3 class="mb-3 align-left">Aggiungi foto</h3>
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
                :customStrings="{
                            upload: '<h1>RECIPEEE!</h1>',
                            drag: 'Drag a 😺 GIF'
                            }"
        >
        </picture-input>
        <br/>
        <br/>
        <h3 class="mb-3 align-left">Aggiungi Passaggi</h3>

        <ul>
            <li v-for="(input, index) in inputs" :key="index">

                <div class="row">
                    <div class="col-12">
                        <!--   <form action="http://localhost:8000/api/questions/"
                                  method="post"
                                  encType="multipart/form-data"
                                > -->

                        <textarea
                                name="content"
                                v-model="input.body"
                                class="form-control"
                                placeholder="Cosa vuoi chiedere?"
                                rows="1"
                        ></textarea>
                        <div class="hello">
                            <picture-input
                                    @change="handleFileChange($event, index)"
                                    name="picture"
                                    ref="file"
                                    width="150"
                                    height="150"
                                    margin="16"
                                    accept="image/jpeg,image/png,image/gif"
                                    size="5"
                                    buttonClass="btn"
                                    :customStrings="{
                            upload: '<h1>RECIPEEE!</h1>',
                            drag: 'Drag a 😺 GIF'
                            }"
                            >
                            </picture-input>
                        </div>
                        <br/>
                    </div>
                </div>

                <button @click="deleteRow(index)" class="child">Delete</button>
            </li>
        </ul>

        <button @click="addRow">Add row</button>
        <button @click="onSubmit" value="Upload!">Upload</button>
        <br/>
        <br/>
        <div class="md-layout-item">
            <md-field>
                <md-select v-model="movie" name="movie" id="movie">
                    <md-option value="fight-club">Fight Club</md-option>
                    <md-option value="godfather">Godfather</md-option>
                    <md-option value="godfather-ii">Godfather II</md-option>
                    <md-option value="godfather-iii">Godfather III</md-option>
                    <md-option value="godfellas">Godfellas</md-option>
                    <md-option value="pulp-fiction">Pulp Fiction</md-option>
                    <md-option value="scarface">Scarface</md-option>
                </md-select>
            </md-field>
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
        name: "QuestionEditor",
        components: {
            PictureInput
        },
        props: {
            slug: {
                type: String,
                error: null
            },
            previousQuestion: {
                type: String,
                required: false
            },
            token: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                movie: "good father",
                inputs: [],
                questionBody: this.previousQuestion || null,
                error: null,
                picture: null
            };
        },

        async beforeRouteEnter(to, from, next) {
            to.params.token = CSRF_TOKEN;
            console.log(to.params.token);

            if (to.params.slug !== undefined) {
                let endpoint = `/api/questions/${to.params.slug}/`;
                await apiService(endpoint).then(data => {
                    to.params.previousQuestion = data.content;
                });
            }
            return next();
        },
        methods: {
            dataURLtoFile(dataurl, filename) {

                var arr = dataurl.split(','),
                    mime = arr[0].match(/:(.*?);/)[1],
                    bstr = atob(arr[1]),
                    n = bstr.length,
                    u8arr = new Uint8Array(n);

                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n);
                }

                return new File([u8arr], filename, {type: mime});
            },
            addRow() {
                this.inputs.push({
                    body: "",
                    picture: null
                });
            },
            deleteRow(index) {
                this.inputs.splice(index, 1);
            },
            handleFileChange(event, index) {
                console.log("New picture selected!");
                if (event) {
                    console.log("Squalo");
                    // document.getElementById("token").setAttribute("value", this.token);
                    //  console.log(document.getElementById("token").getAttribute("value"));

                    console.log("Picture loaded.");
                    this.inputs[index].picture = this.dataURLtoFile(event, this.questionBody + "-picture.jpg");
                    console.log(this.inputs[index].picture);
                } else {
                    console.log("FileReader API not supported: use the <form>, Luke!");
                }
            },
            onChange(event) {
                console.log("New picture selected!");
                if (event) {
                    console.log("Squalo");
                    // document.getElementById("token").setAttribute("value", this.token);
                    //  console.log(document.getElementById("token").getAttribute("value"));

                    console.log("Picture loaded.");
                    this.picture = this.dataURLtoFile(event, this.questionBody + "-picture.jpg");
                    console.log(this.picture);
                } else {
                    console.log("FileReader API not supported: use the <form>, Luke!");
                }
            },
            onSubmit() {
                console.log("token " + CSRF_TOKEN);
                //  axios.defaults.xsrfCookieName = 'csrfmiddlewaretoken'
                //  axios.defaults.xsrfHeaderName = "X-CSRFToken"
                //  axios.defaults.headers.common["X-CSRFToken"] = CSRF_TOKEN;
                const headers = {"X-CSRFTOKEN": CSRF_TOKEN};
                const fd = new FormData();

                fd.append("content", this.questionBody);
                fd.append("picture", this.picture, this.picture.name);
                console.log(fd);
                console.log("body " + this.questionBody);
                console.log(this.picture);
                console.log("picname " + this.picture.name);

                const endpoint = "http://localhost:8000/api/questions/";
                axios
                    .post(endpoint, fd, {headers: headers})
                    .then(question_data => {
                        console.log(question_data.data.slug);
                        this.inputs.forEach(input => {
                            const fp = new FormData();
                            fp.append("body", input.body);
                            fp.append("picture", input.picture);
                            axios.post(endpoint + question_data.data.slug + "/passage/", fp, {headers: headers})
                                .then(res => {
                                    console.log("recipes res");
                                    console.log(res);
                                })
                        });

                    })
                    .catch(err => console.log(err));
            }

            // onSubmit() {
            //   if (!this.questionBody) {
            //     this.error = "Il campo non puo essere vuoto.";
            //   } else if (this.questionBody.length > 240) {
            //     this.error = "Non superare i 240 caratteri.";
            //   } else {
            //     let endpoint = "/api/questions/";
            //     let method = "POST";
            //     if (this.previousQuestion) {
            //       method = "PUT";
            //       endpoint += `${this.slug}/`;
            //     }
            //     apiService(endpoint, method, {content: this.questionBody}).then(
            //       question_data => {
            //         this.$router.push({
            //           name: "question",
            //           params: { slug: question_data.slug }
            //         });
            //       }
            //     );
            //   }
            // }
        },
        created() {
            document.title = "Editor - QuestionPlace";
            console.log("created");
            this.inputs.push({
                body: "",
                image: null
            });
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
        float: right;
    }

    .align-left {
        float: left;
    }
</style>
