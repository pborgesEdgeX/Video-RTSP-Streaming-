FROM denismakogon/gocv-alpine:3.4.2-buildstage as build-stage

#Copy the local package files (from development computer) to the container's workspace (docker image)
COPY . /go/src/app 
# Build the app command inside the container
RUN go install app


FROM denismakogon/gocv-alpine:3.4.2-runtime

#Author label
LABEL Author Paulo Borges

#Copy executable binary file
COPY --from=build-stage /go/bin/app /go/bin/app

#Run executable when container starts
ENTRYPOINT ["/go/bin/app"]
