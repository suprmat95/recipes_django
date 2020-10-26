<template lang="html">
    <div class="question-actions" >
        <router-link
                :to="{name: 'question-editor', params:{slug: slug}}"
        >
            <md-button class="button btn btn-sm ">
                <md-icon>edit</md-icon> Modifica la ricetta
            </md-button>
        </router-link>
        <md-button
                class="button btn btn-sm "
                @click="deleteQuestion">
            <md-icon>delete</md-icon> Cancella la ricetta
        </md-button>
</div>
</template>

<script>
    import {apiService} from "../common/api.service";

    export default {
        name: "QuestionActions",
        props: {
            slug: {
                type: String,
                required: true
            }
        },
        methods: {
            async deleteQuestion() {
                let endpoint = `/api/questions/${this.slug}/`;
                try {
                    await apiService(endpoint, "DELETE");
                    this.$router.push("/home");
                } catch (err) {
                    console.log(err);
                }
            }
        }
    }
</script>

<style lang="css">
    .question-actions{
        display: inline;
        alignment: center;
    }
    .button {
        margin: 10px;
        border: 5px;
    }
</style>