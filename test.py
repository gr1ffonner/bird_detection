from roboflow import Roboflow
rf = Roboflow(api_key="Epq9BGzUuroeUYu2Cl20")
project = rf.workspace().project("birds-detector-tis9s")
model = project.version(1).model


# visualize your prediction
model.predict("birds.jpg", confidence=25, overlap=50).save("prediction.jpg")

# model.predict("birds.jpg", confidence=25, overlap=50).
