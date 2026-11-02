# import shutil
# from pathlib import Path

# import streamlit as st 

# st.set_page_config(page_title="File & Folder Manager", page_icon="📁", layout="wide")

# # All operations happen inside this folder, so nothing outside it can be touched.
# ROOT = Path("storage").resolve()
# ROOT.mkdir(exist_ok=True)


# # ---------- helpers ----------
# def flash(kind: str, msg: str):
#     """Save a message, then rerun so lists refresh and the message shows once."""
#     st.session_state["flash"] = (kind, msg)
#     st.rerun()


# def safe_path(name: str) -> Path:
#     """Turn a user-typed name into a path that is guaranteed to be inside ROOT."""
#     name = name.strip()
#     if not name:
#         raise ValueError("Name cannot be empty.")
#     p = (ROOT / name).resolve()
#     if p == ROOT or ROOT not in p.parents:
#         raise ValueError("Path must stay inside the storage folder.")
#     return p


# def list_folders():
#     return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_dir())


# def list_files():
#     return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())


# # ---------- show pending message ----------
# if "flash" in st.session_state:
#     kind, msg = st.session_state.pop("flash")
#     getattr(st, kind)(msg)


# # ---------- folder section ----------
# def folder_section():
#     t_create, t_read, t_update, t_delete = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])

#     with t_create:
#         with st.form("create_folder", clear_on_submit=True):
#             name = st.text_input("Folder name (use a/b to create nested folders)")
#             if st.form_submit_button("Create folder"):
#                 try:
#                     p = safe_path(name)
#                     if p.exists():
#                         st.error("Folder already exists, try another name.")
#                     else:
#                         p.mkdir(parents=True)
#                         flash("success", f"Folder '{name}' created successfully!")
#                 except ValueError as e:
#                     st.error(str(e))

#     with t_read:
#         items = [p for p in sorted(ROOT.rglob("*"))]
#         if not items:
#             st.info("Storage is empty.")
#         for i, p in enumerate(items, 1):
#             icon = "📁" if p.is_dir() else "📄"
#             st.text(f"{i} : {icon} {p.relative_to(ROOT).as_posix()}")

#     with t_update:
#         folders = list_folders()
#         if not folders:
#             st.info("No folders to rename.")
#         else:
#             with st.form("update_folder", clear_on_submit=True):
#                 old = st.selectbox("Folder to rename", folders)
#                 new = st.text_input("New name (full path inside storage)")
#                 if st.form_submit_button("Rename folder"):
#                     try:
#                         new_p = safe_path(new)
#                         if new_p.exists():
#                             st.error("That name already exists.")
#                         else:
#                             (ROOT / old).rename(new_p)
#                             flash("success", f"Renamed '{old}' to '{new}'.")
#                     except (ValueError, OSError) as e:
#                         st.error(str(e))

#     with t_delete:
#         folders = list_folders()
#         if not folders:
#             st.info("No folders to delete.")
#         else:
#             with st.form("delete_folder"):
#                 target = st.selectbox("Folder to delete", folders)
#                 sure = st.checkbox("Yes, delete this folder and everything inside it")
#                 if st.form_submit_button("Delete folder", type="primary"):
#                     if not sure:
#                         st.warning("Please tick the confirmation box first.")
#                     else:
#                         try:
#                             shutil.rmtree(ROOT / target)
#                             flash("success", f"Folder '{target}' deleted successfully!")
#                         except OSError as e:
#                             st.error(str(e))


# # ---------- file section ----------
# def file_section():
#     t_create, t_read, t_update, t_delete = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])

#     with t_create:
#         with st.form("create_file", clear_on_submit=True):
#             location = st.selectbox("Create inside", ["(root)"] + list_folders())
#             name = st.text_input("File name with extension (e.g. notes.txt)")
#             data = st.text_area("File content", height=200)
#             if st.form_submit_button("Create file"):
#                 try:
#                     rel = name.strip() if location == "(root)" else f"{location}/{name.strip()}"
#                     p = safe_path(rel)
#                     if p.exists():
#                         st.error("File name already exists, please try another.")
#                     else:
#                         p.write_text(data, encoding="utf-8")
#                         flash("success", f"File '{rel}' created successfully!")
#                 except (ValueError, OSError) as e:
#                     st.error(str(e))

#     with t_read:
#         files = list_files()
#         if not files:
#             st.info("No files yet.")
#         else:
#             choice = st.selectbox("Which file do you want to read?", files, key="read_choice")
#             p = ROOT / choice
#             try:
#                 st.code(p.read_text(encoding="utf-8"), language=None)
#             except UnicodeDecodeError:
#                 st.warning("This is a binary file and can't be shown as text.")
#                 st.download_button("Download file", p.read_bytes(), file_name=p.name)

#     with t_update:
#         files = list_files()
#         if not files:
#             st.info("No files to update.")
#         else:
#             choice = st.selectbox("Choose a file", files, key="update_choice")
#             p = ROOT / choice
#             action = st.radio(
#                 "What do you want to do?",
#                 ["Change the name", "Overwrite the content", "Append new content"],
#                 horizontal=True,
#             )

#             if action == "Change the name":
#                 with st.form("rename_file", clear_on_submit=True):
#                     new = st.text_input("New name with extension (full path inside storage)")
#                     if st.form_submit_button("Rename"):
#                         try:
#                             new_p = safe_path(new)
#                             if new_p.exists():
#                                 st.error("That name already exists.")
#                             else:
#                                 p.rename(new_p)
#                                 flash("success", "File name changed successfully!")
#                         except (ValueError, OSError) as e:
#                             st.error(str(e))

#             elif action == "Overwrite the content":
#                 try:
#                     current = p.read_text(encoding="utf-8")
#                 except UnicodeDecodeError:
#                     current = None
#                     st.warning("Binary file, can't edit as text.")
#                 if current is not None:
#                     with st.form("overwrite_file"):
#                         data = st.text_area("New content", value=current, height=250)
#                         if st.form_submit_button("Overwrite"):
#                             p.write_text(data, encoding="utf-8")
#                             flash("success", "Overwritten successfully!")

#             else:
#                 with st.form("append_file", clear_on_submit=True):
#                     data = st.text_area("Content to append", height=150)
#                     if st.form_submit_button("Append"):
#                         try:
#                             with open(p, "a", encoding="utf-8") as fs:
#                                 fs.write(data)
#                             flash("success", "Appended successfully!")
#                         except OSError as e:
#                             st.error(str(e))

#     with t_delete:
#         files = list_files()
#         if not files:
#             st.info("No files to delete.")
#         else:
#             with st.form("delete_file"):
#                 target = st.selectbox("File to delete", files)
#                 sure = st.checkbox("Yes, delete this file permanently")
#                 if st.form_submit_button("Delete file", type="primary"):
#                     if not sure:
#                         st.warning("Please tick the confirmation box first.")
#                     else:
#                         try:
#                             (ROOT / target).unlink()
#                             flash("success", f"File '{target}' deleted successfully!")
#                         except OSError as e:
#                             st.error(str(e))


# # ---------- main layout ----------
# st.title("📁 File & Folder Manager")
# st.caption(f"Working inside: `{ROOT}`")

# with st.sidebar:
#     st.header("Menu")
#     section = st.radio("Manage", ["Folders", "Files"])
#     st.divider()
#     st.metric("Folders", len(list_folders()))
#     st.metric("Files", len(list_files()))

# if section == "Folders":
#     st.subheader("Folder operations")
#     folder_section()
# else:
#     st.subheader("File operations")
#     file_section()