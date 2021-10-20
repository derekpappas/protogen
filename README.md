# protogen
convert JSON to proto to swagger to Java

# Python virtualenv setup
mkvirtualenv swagger_gen
workon swagger_gen
pip3 install GitPython
pip3 install gitpython


# Inspired by:
github.com/bbengfort/notes
###### protobuf install
https://medium.com/@danny4410.eecs04/install-protobuf-on-m1-mac-852e4afa619f
/bin/bash -c “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH=/opt/homebrew/bin:$PATH
git clone https://github.com/protocolbuffers/protobuf.git
brew install autoconf
brew install automake
brew install Libtool
autoreconf -i
./autogen.sh
./configure
make
make check
sudo make install
export PATH=/opt/usr/local/bin:$PATH


###### OpenAPI specification

https://swagger.io/resources/open-api/

###### go installation

brew install go

###### Building GRPC Java

git clone git@github.com:grpc/grpc-java.git

cd grpc-java

#https://github.com/grpc/grpc-java/blob/v1.41.0/COMPILING.md

./gradlew build
./gradlew publishToMavenLocal
###### proton installation

brew install protobuf

protoc --version

###### bazel installation

brew install bazel

# https://github.com/grpc-ecosystem/grpc-gateway

git clone git@github.com:grpc-ecosystem/grpc-gateway.git

cd grpc-gateway

go install \
github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway \
github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2 \
google.golang.org/protobuf/cmd/protoc-gen-go

cd $HOME/grpc-gateway/protoc-gen-openapiv2

bazel build

./gradlew publishToMavenLocal

cd examples

./gradlew installDist

###### 

rotoc-I ./proto/ \
    -I include/googleapis -I include/grpc-gateway \
    --go_out=. --go_opt=module=github.com/bbengfort/notes \
    --go-grpc_out=. --go-grpc_opt=module=github.com/bbengfort/notes \
    --openapiv2_out ./openapiv2 --openapiv2_opt logtostderr=true \
    proto/notes/v1/*.proto

https://grpc-ecosystem.github.io/grpc-gateway/docs/mapping/customizing_openapi_output/

git@github.com:grpc-ecosystem/grpc-gateway.git

https://bbengfort.github.io/2021/01/grpc-openapi-docs/



