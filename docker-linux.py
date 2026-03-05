import streamlit as st
import docker
import subprocess

st.set_page_config(page_title="Docker + Linux Dashboard", layout="wide")

client = docker.from_env()

st.title(" Docker + Linux Dashboard")

menu = st.sidebar.selectbox("Select Option", [
    "Containers",
    "Images",
    "Build Image",
    "Create Container",
    "Container Logs",
    "Linux Commands"
])

# -------------------- CONTAINERS --------------------

if menu == "Containers":
    st.header("all Containers")

    containers = client.containers.list(all=True)

    for container in containers:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(container.name)
        col2.write(container.status)

        if col3.button("Start", key=f"start_{container.id}"):
            container.start()
            st.success(f"{container.name} started")

        if col4.button("Stop", key=f"stop_{container.id}"):
            container.stop()
            st.warning(f"{container.name} stopped")

        if col5.button("Restart", key=f"restart_{container.id}"):
            container.restart()
            st.info(f"{container.name} restarted")

        if st.button("Remove", key=f"remove_{container.id}"):
            container.remove(force=True)
            st.error(f"{container.name} removed")

# -------------------- IMAGES --------------------

elif menu == "Images":
    st.header("Docker Images")

    images = client.images.list()

    for image in images:
        st.write(image.tags)

    image_name = st.text_input("Pull Image (example: nginx:latest)")
    if st.button("Pull Image"):
        client.images.pull(image_name)
        st.success("Image Pulled Successfully ")

# -------------------- BUILD IMAGE --------------------

elif menu == "Build Image":
    st.header("Build Docker Image")

    dockerfile_path = st.text_input("Dockerfile Path (example: ./app)")
    image_tag = st.text_input("Image Tag (example: myapp:latest)")

    if st.button("Build"):
        client.images.build(path=dockerfile_path, tag=image_tag)
        st.success("Image Built Successfully ")

# -------------------- CREATE CONTAINER --------------------

elif menu == "Create Container":
    st.header("Create New Container")

    image = st.text_input("Image Name (example: nginx:latest)")
    name = st.text_input("Container Name")
    port = st.text_input("Port Mapping (example: 8080:80)")

    if st.button("Create"):
        port_mapping = {}
        if port:
            host, container_port = port.split(":")
            port_mapping = {container_port: host}

        container = client.containers.run(
            image,
            name=name,
            ports=port_mapping,
            detach=True
        )
        st.success("Container Created ")

# -------------------- LOGS --------------------

elif menu == "Container Logs":
    st.header("View Container Logs")

    containers = client.containers.list(all=True)
    container_names = [c.name for c in containers]

    selected = st.selectbox("Select Container", container_names)

    if st.button("Show Logs"):
        container = client.containers.get(selected)
        logs = container.logs().decode("utf-8")
        st.code(logs)

# -------------------- LINUX COMMANDS --------------------

elif menu == "Linux Commands":
    st.header("Basic Linux Commands")

    cmd = st.text_input("Enter Linux Command")

    if st.button("Run Command"):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            st.code(result.stdout)
        except Exception as e:
            st.error(str(e))
