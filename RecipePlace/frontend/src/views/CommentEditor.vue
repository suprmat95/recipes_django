<template>
    <div class="container mt-2">
        <div class="row">
            <div class="col-12">
                <h1 class="mb-3">Modifica la tua risposta</h1>
                <form @submit.prevent="onSubmit">
                    <textarea v-model="commentBody"
                              class="form-control"
                              rows="3"
                    ></textarea>
                    <br>
                    <button
                        class="btn btn-success"
                        type="submit"
                    >Pubblica Risposta
                    </button>
                </form>
                <p class="error mt-2">{{error}}</p>
            </div>
        </div>
    </div>

</template>

<script>
    import {apiService} from "../common/api.service";

    export default {
        name: "CommentEditor",
        props: {
            id: {
                type: Number,
                required: true
            },
            previousComment: {
                type: String,
                required: true
            },
            recipeSlug:{
                type: String,
                required: true
            }
        },
        async beforeRouteEnter(to, from, next) {
            let endpoint =`/api/comment/${to.params.id}/`;
            await apiService(endpoint)
                    .then(data=>{
                        console.log("commento: ")
                        console.log(data)
                        to.params.previousComment = data.body;
                        to.params.recipeSlug = data.recipe_slug;
                    })
            return next();
            },
        data() {
            return {
                commentBody: this.previousComment,
                error: null
            }
        },
        methods: {
            onSubmit() {
                if (this.commentBody) {
                    let endpoint = `/api/comment/${this.id}/`;
                    apiService(endpoint, "PUT", {body: this.commentBody})
                        .then(()=> {
                            this.$router.push({
                                name: "recipe",
                                params: {slug: this.recipeSlug}
                            })
                        })

                } else {
                    this.error = "Il campo non puo essere vuoto";
                }
            }
        }
    }
</script>

<style lang="css">

</style>