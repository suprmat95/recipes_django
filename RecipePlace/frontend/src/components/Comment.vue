<template lang="html">
    <div class="single-comment">
        <p class="text-muted">
            <strong>{{comment.author}}</strong> ha risposto il {{comment.created_at}}
        </p>
        <p class="commento">{{comment.body}}</p>
        <div v-if="isCommentAuthor" class="comment-owner">
            <router-link
                    :to="{name:'comment-editor', params: {id: comment.id}}"
                    >
                 <md-button class="button btn btn-sm ">
                <md-icon>edit</md-icon> Modifica il commento
            </md-button>
            </router-link>
            <md-button
                class="button btn btn-sm "
                @click="triggerDeleteComment">
            <md-icon>delete</md-icon> Cancella il commento
        </md-button>


        </div>
        <div v-else class="like-comment">
            <button
                    class="btn btn-sm"
                    @click="toggleLike"
                    :class="{
                        'btn-danger': userLikedComment,
                        'btn-outline-danger': !userLikedComment,
                    }">
                <md-icon>thumb_up</md-icon> <strong> Mi piace [{{likesNumber}}]</strong>
            </button>
        </div>
    </div>

</template>

<script>
    import {apiService} from "../common/api.service";

    export default {
        name: "CommentComponent",
        props: {
            comment: {
                type: Object,
                required: true
            },
            requestUser: {
                type: String,
                required: true
            }
        },
        data (){
            return{
                userLikedComment: this.comment.user_has_voted,
                likesNumber: this.comment.likes_count
            }
        },
        computed: {
            isCommentAuthor() {
                return this.comment.author === this.requestUser;
            }
        },
        methods: {
            toggleLike() {
                this.userLikedComment===false
                    ? this.likeComment()
                    : this.unLikeComment()
            },
            likeComment() {
                this.userLikedComment =true;
                this.likesNumber+=1;
                let endpoint = `/api/comments/${this.comment.id}/like/`;
                apiService(endpoint, "POST");
            },
            unLikeComment() {
                this.userLikedComment =false;
                this.likesNumber-=1;
                let endpoint = `/api/comments/${this.comment.id}/like/`;
                apiService(endpoint, "DELETE");
            },
            triggerDeleteComment() {
                this.$emit("delete-comment",this.comment)
            }
        }
    }
</script>

<style scoped>
.commento {
    border: 3px solid lightgrey;
    border-radius: 5px;
    width: 40%;
    height: 50px;
background: rgb(177,246,255);
background: radial-gradient(circle, rgba(177,246,255,1) 0%, rgba(240,250,226,1) 100%);}
</style>