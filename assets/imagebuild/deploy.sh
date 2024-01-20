
#!/bin/bash

export AnException=100
export AnotherException=101

execute_python() {
    echo "Starting the script at " `date`
    cd $1
    python main.py
    aws s3 cp . $2 --recursive --exclude "*" --include="*.csv"
    cd ../
}

function try()
{
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

function throw()
{
    exit $1
}

function catch()
{
    export ex_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $ex_code
}

function throwErrors()
{
    set -e
}

function ignoreErrors()
{
    set +e
}


# start with a try
try
(
    echo "Start the try statement"
    execute_python photolithography-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/photolithography-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python etching-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/etching-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python chemical-vapor-deposition-cvd-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/chemical-vapor-deposition-cvd-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python physical-vapor-deposition-pvd-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/physical-vapor-deposition-pvd-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python ion-implantation-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/ion-implantation-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python diffusion-furnace s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/diffusion-furnace/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python wet-bench s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/wet-bench/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python wire-bonding-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/wire-bonding-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python die-attach-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/die-attach-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
# start with a try
try
(
    echo "Start the try statement"
    execute_python packaging-machine s3://synthetic-data-backend-data-246882249665-us-east-1/wallnm-2308/packaging-machine/ || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}
