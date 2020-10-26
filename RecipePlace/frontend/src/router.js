import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue"
import Recipe from "./views/Recipe.vue";
import RecipeEditor from "./views/RecipeEditor";
import CommentEditor from "./views/CommentEditor";

Vue.use(Router);

export default new Router({
    mode: "history",
    routes: [
        {
            path: "/home",
            name: "home",
            component: Home
        },
        {
            path: "/home/recipe/:slug",
            name: "recipe",
            component: Recipe,
            props: true
        },
        {
            path: "/home/comment/:id",
            name: "comment-editor",
            component: CommentEditor,
            props: true
        },
        {
            path: "/home/ask/:slug?",
            name: "recipe-editor",
            component: RecipeEditor,
            props: true
        },
       // {
       //     path: "*/media",
       //     name: "page-not-found",
       //     component: NotFound
       //  },

    ]
});