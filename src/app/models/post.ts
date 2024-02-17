export interface Post {
    id: string,
    title: string,
    text: string,
    publishedDate: Date,
    userId: string,
    categoryId: string,
    likes: number,
}

export interface AddPost {
    title: string,
    text: string,
    categoryId: string,
}

export interface GetPosts {
    posts: Post[],
    totalPages: number,
}
