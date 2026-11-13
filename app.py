
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="The Caregiver Circle",
    page_icon="🌿",
    layout="centered"
)

DB_PATH = r"C:\Users\tuf81\discussion_board.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_discussions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, post, created_at
    FROM discussions
    ORDER BY created_at DESC
    """)

    discussions = cursor.fetchall()
    conn.close()

    return discussions


def create_discussion(title, post):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO discussions (title, post)
    VALUES (?, ?)
    """, (title, post))

    conn.commit()
    conn.close()


def get_comments(discussion_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, comment, created_at
    FROM comments
    WHERE discussion_id = ?
    ORDER BY created_at ASC
    """, (discussion_id,))

    comments = cursor.fetchall()
    conn.close()

    return comments


def add_comment(discussion_id, comment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO comments (discussion_id, comment)
    VALUES (?, ?)
    """, (discussion_id, comment))

    conn.commit()
    conn.close()


# COMMUNITY HOMEPAGE

st.title("🌿 The Caregiver Circle")

st.write(
    "A welcoming community for caregivers "
    "to connect, share experiences, and support one another."
)

st.divider()

st.header("Start a Discussion")

with st.form("new_discussion"):
    title = st.text_input("Discussion title")

    post = st.text_area(
        "What's on your mind?",
        height=150
    )

    submitted = st.form_submit_button("Publish Discussion")

    if submitted:
        if title.strip() and post.strip():
            create_discussion(title.strip(), post.strip())
            st.success("Your discussion has been published!")
            st.rerun()
        else:
            st.warning("Please enter a title and discussion.")

st.divider()

st.header("Community Discussions")

discussions = get_discussions()

if not discussions:
    st.info("Be the first to start a discussion!")

for discussion in discussions:

    discussion_id = discussion[0]

    with st.container(border=True):

        st.subheader(discussion[1])
        st.write(discussion[2])

        st.caption(f"Posted: {discussion[3]}")

        st.write("**Comments**")

        comments = get_comments(discussion_id)

        if comments:
            for comment in comments:
                st.write(comment[1])
                st.caption(f"Posted: {comment[2]}")
        else:
            st.caption("No comments yet.")

        with st.form(f"comment_form_{discussion_id}"):

            new_comment = st.text_area(
                "Add a comment",
                key=f"comment_{discussion_id}"
            )

            comment_submitted = st.form_submit_button("Post Comment")

            if comment_submitted:
                if new_comment.strip():
                    add_comment(discussion_id, new_comment.strip())
                    st.success("Comment posted!")
                    st.rerun()
                else:
                    st.warning("Please enter a comment.")
