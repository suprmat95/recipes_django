<template lang="html">
    <div class="recioe-actions" >
        <router-link
                :to="{name: 'recipe-editor', params:{slug: slug}}"
        >
            <md-button class="button btn btn-sm ">
                <md-icon>edit</md-icon> Modifica la ricetta
            </md-button>
        </router-link>
        <md-button
                class="button btn btn-sm "
                @click="deleteRecipe">
            <md-icon>delete</md-icon> Cancella la ricetta
        </md-button>
</div>
</template>

<script>
    import {apiService} from "../common/api.service";

    export default {
        name: "RecipeActions",
        props: {
            slug: {
                type: String,
                required: true
            }
        },
        methods: {
            async deleteRecipe() {
                let endpoint = `/api/recipes/${this.slug}/`;
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
    .recipe-actions{
        display: inline;
        alignment: center;
    }
    .button {
        margin: 10px;
        border: 5px;
    }
</style>