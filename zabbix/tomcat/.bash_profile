# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin
JAVA_HOME=/usr/java/jdk1.7.0_55
PATH=$JAVA_HOME/bin:$PATH:$HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar
export PATH JAVA_HOME CLASSPATH CATALINA_HOME


export PATH

