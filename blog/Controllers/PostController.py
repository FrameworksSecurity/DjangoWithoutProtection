from django.shortcuts import render, redirect
from blog.Models.Post import Post
from blog.Models.Comment import Comment
from django.db import connection
from datetime import datetime
import mysql.connector

class PostController:
    @staticmethod
    def list(request):
        data = {}
        data["title"] = "Posts"
        data["description"] = "List of Posts"
        data["posts"] = Post.objects.all()
        return render(request, "post/list.html", {"data": data})

    @staticmethod
    def show(request, postid):
        data = {}
        post = Post.objects.get(id=postid)
        data["title"] = post.getTitle()
        data["description"] = post.getDescription()
        data["post"] = post
        return render(request, "post/show.html", {"data": data})

    @staticmethod
    def save(request):
        cnx = mysql.connector.connect(user='root', database='blog_django')
        cursor = cnx.cursor()
        if request.method == "POST":
            title = request.POST.get("title")
            description= request.POST.get("description")
            created_at= datetime.now()
            updated_at = datetime.now()
            query="INSERT INTO blog_post (created_at, updated_at, title, description) VALUES('%s', '%s', '%s', '%s')" % (created_at, updated_at,title, description)
            cursor.execute(query, multi=True)
            return redirect("/posts")
        else:
            return redirect("/posts")

    @staticmethod
    def saveComment(request):
        if request.method == "POST":
            post = Post.objects.get(id=request.POST.get("post_id"))
            post_id = request.POST.get("post_id")
            newComment = Comment()
            newComment.post = post
            newComment.setMessage(request.POST.get("message"))
            newComment.clean()
            newComment.save()
        return redirect("/posts/"+post_id)

    @staticmethod
    def deleteComment(request, commentid):
        post_id = request.POST.get("post_id")
        comments = Comment.objects.get(id=commentid)
        comments.delete()
        return redirect("/posts/"+post_id)
