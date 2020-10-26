<template lang="html">
    <div class="single-question mt-2">
        <div v-if="notFound" class="container">
            <h1>Ricetta non trovata!</h1>
        </div>
        <div v-else class="container">
            <div class="container">
                <div align="right">
                <QuestionActions v-if="isOwner" :slug="slug" />
                </div>
                <br/>
                <br/>
                <div align="center">
                    <img  align="center" id="picture" width="500" height="500"/>
                </div>
                <br/>
                <h1>{{ question.content }}</h1>
                <h5>{{question.description}}</h5>
                <hr/>

                <h2 class="mb-3 align-left">Ingredienti</h2>
                <div class="row">
                    <div class="col-sm">
                        <ul>
                            <li v-for="(ingredient, index) in ingredients" :key="index">
                                <h5
                                >{{ ingredient.name }} {{ ingredient.quantity }}
                                    {{ ingredient.unity }}</h5>

                            </li>
                        </ul>
                    </div>
                </div>
                <br/>
                <hr/>
                <h2 class="mb-3 align-left">Passaggi</h2>

                    <div v-for="(passage, index) in passages" :key="'A' + index">
                        <md-card>

                            <md-card-media>
                                <img :src="passage.picture" alt="People">
                            </md-card-media>
                            <div class="md-title"> Passagio {{index +1}} <br/></div>

                            <md-card-content>
                                <b>{{ passage.body }}</b>
                            </md-card-content>
                        </md-card>
                        <br/>
                        <br/>
                    </div>


                <p class="mb-0">
                    Ricetta aggiunta da:
                    <span class="author-name">{{ question.author }}</span>
                </p>
                <p>{{ question.created_at }}</p>
                <hr/>
                <template v-if="userHasAnswered">
                    <p class="answer-added">Hai commentanto questa ricetta.</p>
                </template>
                <template v-else-if="showForm">
                    <form class="card" @submit.prevent="onSubmit">
                        <div class="card-header px-3">
                            Aggiungi un commento alla ricetta
                        </div>
                        <div class="card-block">
              <textarea
                      v-model="newAnswerBody"
                      class="form-control"
                      placeholder="Aggiungi un commento alla ricetta"
                      rows="5"
              ></textarea>
                        </div>
                        <div class="card-footer px-3">
                            <button type="submit" class="btn btn-sm btn-success">
                                Aggiungi Commento
                            </button>
                        </div>
                    </form>
                    <p class="error mt-2">{{ this.error }}</p>
                </template>
                <template v-else>
                    <button class="btn btn-sm btn-success" @click="showForm = true">
                        Commenta la ricetta
                    </button>
                </template>
                <hr/>
                <AnswerComponent
                        v-for="(answer, index) in answers"
                        :answer="answer"
                        :requestUser="requestUser"
                        :key="index"
                        @delete-answer="deleteAnswer"
                />
                <div class="my-4">
                    <p v-show="loadingAnswers">...loading...</p>
                    <button
                            v-show="next"
                            @click="getQuestionAnswers"
                            class="btn btn-sm btn-outline-succes"
                    >
                        Carica Ancora
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {apiService} from "../common/api.service";
    import AnswerComponent from "../components/Answer";
    import QuestionActions from "../components/QuestionActions";

    export default {
        name: "Question",

        props: {
            slug: {
                type: String,
                required: true
            }
        },
        components: {
            QuestionActions,
            AnswerComponent
        },
        data() {
            return {
                question: {},
                loadingAnswers: false,
                answers: [],
                ingredients: [],
                passages: [],
                userHasAnswered: false,
                showForm: false,
                newAnswerBody: null,
                error: null,
                next: null,
                requestUser: null
            };
        },
        computed: {
            isOwner() {
                return this.question.author === this.requestUser;
            },
            notFound() {
                return this.question["detail"];
            }
        },
        methods: {
            setPageTitle(title) {
                document.title = title;
            },
            setRequestUser() {
                this.requestUser = window.localStorage.getItem("username");
            },
            getQuestionData() {
                let endpoint = `/api/questions/${this.slug}/`;
                apiService(endpoint).then(data => {
                    this.question = data;
                    console.log(this.question.passage);
                    this.ingredients = this.question.ingredient;
                    this.passages = this.question.passage;
                    document
                        .getElementById("picture")
                        .setAttribute("src", this.question.picture);

                    this.userHasAnswered = data.user_has_answered;
                    this.setPageTitle(data.content);
                });
            },
            getQuestionAnswers() {
                let endpoint = `/api/questions/${this.slug}/answers/`;
                if (this.next) {
                    endpoint = this.next;
                }
                this.loadingAnswers = true;
                apiService(endpoint).then(data => {
                    this.answers.push(...data.results);
                    this.loadingAnswers = false;
                    if (data.next) {
                        this.next = data.next;
                    } else {
                        this.next = null;
                    }
                });
            },
            onSubmit() {
                console.log(this.newAnswerBody);

                if (this.newAnswerBody) {
                    let endpoint = `/api/questions/${this.slug}/answer/`;

                    apiService(endpoint, "POST", {body: this.newAnswerBody}).then(
                        data => {
                            this.answers.unshift(data);
                            console.log(this.answers);
                        }
                    );
                    this.newAnswerBody = null;
                    this.showForm = false;
                    this.userHasAnswered = true;
                    if (this.error) {
                        this.error = null;
                    }
                } else {
                    this.error = "Il campo non puo essere vuoto.";
                }
            },
            async deleteAnswer(answer) {
                let endpoint = `/api/answers/${answer.id}/`;
                try {
                    await apiService(endpoint, "DELETE");
                    //  this.answers.splice(this.answers.indexOf(answer), 1);
                    this.$delete(this.answers, this.answers.indexOf(answer));
                    this.userHasAnswered = false;
                } catch (err) {
                    console.log(err);
                }
            }
        },
        created() {
            this.getQuestionData();
            this.getQuestionAnswers();
            this.setRequestUser();
        }
    };
</script>

<style scoped>
    .single-question {
        text-align: left;
    }

    .error {
        color: red;
        font-weight: bold;
    }

    .answer-added {
        color: green;
        font-weight: bold;
    }
</style>
