######################################################################
# FS BUILD SYSTEM
# Welcome to the CMake build system for FS.
# by Orient 2014/03/02
######################################################################

######################################################################

cmake_minimum_required(VERSION 2.6)

######################################################################

PROJECT(Engine)

MESSAGE(STATUS "######## PROJECT_SOURCE_DIR: "${PROJECT_SOURCE_DIR})
MESSAGE(STATUS "######## BINARY_DIR: "${PROJECT_BINARY_DIR})

IF(CMAKE_BUILD_TYPE STREQUAL "")
  # CMake defaults to leaving CMAKE_BUILD_TYPE empty. This screws up
  # differentiation between debug and release builds.
  set(CMAKE_BUILD_TYPE "RelWithDebInfo" CACHE STRING "Choose the type of build, options are: None (CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel." FORCE)
ENDIF()
MESSAGE(STATUS "######## CMAKE_BUILD_TYPE: "${CMAKE_BUILD_TYPE})

######################################################################

MESSAGE(STATUS "######## Define")


ADD_DEFINITIONS("
    -std=gnu++98
    -D_SERVER
    -D_STANDALONE
    -D_BUILDING
    -D__linux
    -D_USEITEMPILE
    -D_USENEWNET 
    -DADT_X 
    -DBISHOP_DISPATCHMAP
    -D_WAIT_CITY_DATA_
	-DGS_NOGM
    -DFS_LANG=0
	-DSECOND_EDITION_INSTANCE
	-DSECOND_EDITION_WORLDBOSS
	-D_EQUIPMENT
	-DSECOND_EDITION_COIN
	-DSECOND_EDITION_TRANSFER_WAR
	-DSECOND_EDITION_LIVE_SKILL
	-DSECOND_EDITION_SHORT_BATTLE
	-DSECOND_EDITION_MULTI_RESOLUTION
	-DMEM_DEBUG
")
######################################################################
 MESSAGE(STATUS "using 32bits Build")  
 SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -m32")  
 SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m32")  
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
set (CMAKE_CXX_FLAGS "--std=gnu++98 ${CMAKE_CXX_FLAGS}")
endif ()
 SET(CMAKE_LD_FLAGS "${CMAKE_LD_FLAGS} -m32")  
######################################################################

MESSAGE(STATUS "######## Header")

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})
IF(UNIX)
	INCLUDE_DIRECTORIES("/usr/include")
ENDIF()

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/..)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Share/Header)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Share/Header/Engine)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Share/Header/Common)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Share/Header/Common/NewRelay)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Server/Linux)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Base/Common)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/../../Client/Core/Src)
######################################################################

MESSAGE(STATUS "######## Source")

SET(SRC_LIST 
GameServer.cpp
KSOServer.cpp
)

######################################################################

MESSAGE(STATUS "######## Link")

######################################################################

MESSAGE(STATUS "######## Output")

string(TOLOWER ${CMAKE_BUILD_TYPE} _my_build_type)
IF(_my_build_type STREQUAL debug)
	set(_MY_OUTPUT_NAME "GameServerD")
ELSE()
	set(_MY_OUTPUT_NAME "GameServer")
ENDIF()


IF(_my_build_type STREQUAL debug)
	IF(UNIX)
		set(_MY_OUTPUT_COPY_DST_DIR "${PROJECT_BINARY_DIR}/../../../Share/llibd")
	ELSE()
		set(_MY_OUTPUT_COPY_DST_DIR "${PROJECT_BINARY_DIR}/../../../Share/lib/Debug")
	ENDIF()
ELSE()
	IF(UNIX)
		set(_MY_OUTPUT_COPY_DST_DIR "${PROJECT_BINARY_DIR}/../../../Share/llib")
	ELSE()
		set(_MY_OUTPUT_COPY_DST_DIR "${PROJECT_BINARY_DIR}/../../../Share/lib/Release")
	ENDIF()
ENDIF()

set(_BIN_OUTPUT_COPY_DST_DIR "${PROJECT_BINARY_DIR}/../../../Bin/")

SET(EXECUTABLE_OUTPUT_PATH ${_MY_OUTPUT_COPY_DST_DIR})
ADD_EXECUTABLE(${_MY_OUTPUT_NAME} ${SRC_LIST})
IF(_my_build_type STREQUAL debug)
	TARGET_LINK_LIBRARIES (${_MY_OUTPUT_NAME} pthread ${_MY_OUTPUT_COPY_DST_DIR}/libCoreD.a ${_MY_OUTPUT_COPY_DST_DIR}/libNetModD.a ${_MY_OUTPUT_COPY_DST_DIR}/libEngineD.a ${_MY_OUTPUT_COPY_DST_DIR}/libCommonD.a ${_MY_OUTPUT_COPY_DST_DIR}/libLuaD.a ${_MY_OUTPUT_COPY_DST_DIR}/libkeylog.a)
ELSE()
	TARGET_LINK_LIBRARIES (${_MY_OUTPUT_NAME} pthread ${_MY_OUTPUT_COPY_DST_DIR}/libCore.a ${_MY_OUTPUT_COPY_DST_DIR}/libNetMod.a ${_MY_OUTPUT_COPY_DST_DIR}/libEngine.a ${_MY_OUTPUT_COPY_DST_DIR}/libCommon.a ${_MY_OUTPUT_COPY_DST_DIR}/libLua.a ${_MY_OUTPUT_COPY_DST_DIR}/libkeylog.a)
ENDIF()
######################################################################

MESSAGE(STATUS "######## PostBuild")


add_custom_command(
		TARGET ${_MY_OUTPUT_NAME}
		POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E copy "$<TARGET_FILE:${_MY_OUTPUT_NAME}>" "${_BIN_OUTPUT_COPY_DST_DIR}/$<TARGET_FILE_NAME:${_MY_OUTPUT_NAME}>"
		COMMENT "######Copying to output directory"
		)