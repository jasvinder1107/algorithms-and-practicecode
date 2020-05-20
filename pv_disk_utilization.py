#!/usr/bin/env python3
import sys
import os
import argparse
import json
import logging
import logging.handlers



# need to export path to configuration file. should work faster
if os.getenv("KUBECONFIG") is not None:
    CONFIG = "KUBECONFIG={}".format(os.environ["KUBECONFIG"])
else:
    CONFIG = "KUBECONFIG=/etc/kubernetes/admin/kubeconfig.yaml"
if os.getenv("KUBECTL") is not None:
    KUBECTL = os.environ["KUBECTL"]
else:
    KUBECTL = "/usr/local/bin/kubectl"

OPTIONS = {
           'read': "-o json",
           'ns': "-n",
           'exec': ""
          }

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

kubectl = "{config} {kubectl} {options} {namespace}".format(config=CONFIG,
                                                            kubectl=KUBECTL,
                                                            namespace=OPTIONS["ns"],
                                                            options=OPTIONS["read"])


OK       = 0    # 0 - Service is OK
FAILEDHOST = 1  # 1 - service is not running on some hosts.
CRITICAL = 2    # 2 - Service is in a CRITICAL status.
UNKNOWN  = 3    # 3 - Service status is UNKNOWN

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    """ parse arguments of script """

    logger.debug("Parsing arguments")
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                     formatter_class=CustomFormatter)
    g = parser.add_argument_group("monitoring settings")
    g.add_argument("--application", "-a", action="store",
                   help="Application specification of the pod",required=True)
    g.add_argument("--component", "-co", action="store",
                   help="component specification of the pod",required=True)
    g.add_argument("--namespace", "-n",  action="store",
                   help="namespace of application",required=True)
    g.add_argument("--maxutilization","-mu",action="store",
                   help="max percent utilization highmark",required=False)
    # configuration options
    g.add_argument("--bin", "-e", action="store_const",
                   const=KUBECTL,
                   help="path to kubectl binary")
    g.add_argument("--config", "-c", action="store_const",
                   const=CONFIG,
                   help="path to kubectl config")

    # debug options
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true",
                   default=False, help="enable debugging")
    g.add_argument("--silent", "-s", action="store_true",
                   default=False, help="don't log into console")
    return parser.parse_args(args)


def setup_logging(options):
    """ configure logging """

    logger.debug("Configuring logging")
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
        root.addHandler(ch)


def pv_utilization(application,component,namespace,maxpercent):
    """
     This function utilizes the PV disk utilization of the pods. The function takes the following arguments.        
     1. Application: This is an application specification that uniquely identifies the pod.        
     2. Component: This is a component specification that uniquely identifies the pod.        
     3. namespace: The k8 namespace of the pod the PV is attached.        
     4. maxpercernt: The user-defined Highmark in percent, this variable is used to set max allowed utilization of any of the POD. The default is 80%.
    
    """
    k8_hosts = []
    failed_host = []
    podname_host_keypair =  {}
    result = {}
    return_code = 9999

    k8_hosts_cmd = "{command} {ns} get pods -l application={app},component={comp}|grep nodeName".format(
            command=kubectl,
            ns=namespace,
            app=application,
            comp=component) + "|awk -F':' '{print $2}'|tr -d ',' |tr -d '\"'"

    logger.debug("Command used to get the pods is {hcmd}".format(hcmd=k8_hosts_cmd))

    try: 
        k8_hosts = os.popen(k8_hosts_cmd).read().strip().split("\n")

        logger.debug("Pods are running on hosts {hs}".format(hs=k8_hosts))
    except Exception as e:
        logger.error("Failed to get k8 host for the pods {excetion}".format(exception=e))
    
    try:
        podname_hostname_cmd = "{command} {ns} get pods -l application={app},component={comp}|egrep 'hostname|nodeName'|grep -v topologyKey".format(
                command=kubectl,
                ns=namespace,
                app=application,
                comp=component) + "|awk -F':' '{print $2}'|tr -d ',' |tr -d '\"'|tr -d '\ '|sed '$!N;s/\\n/:/'"
    
        pod_host_key_pair = os.popen(podname_hostname_cmd).read().strip().split("\n")
    
        for podnames_hostnames in pod_host_key_pair:
            podname_hostname_list = podnames_hostnames.split(":")
            podname_host_keypair.update({podname_hostname_list[1]:podname_hostname_list[0]})
        logger.debug("value of podname_host_keypair is {phkp}".format(phkp=podname_host_keypair))
    except Exception as e:
        logger.error("Failed to compile the k8 host,podname keypair can't continue {exception}".format(exception=e))

    for host in k8_hosts:
       if host:
         pv_capacity_curl = "curl -s {h}:10255/metrics |grep {ns}|grep -i {app}|grep -v backup|grep kubelet_volume_stats_capacity_bytes".format(
                 h=host,
                 ns=namespace,
                 app=application) + "|awk '{print $2}'"
         pv_utilization_curl = "curl -s {h}:10255/metrics |grep  {ns}|grep -i {app}|grep -v backup|grep kubelet_volume_stats_used_bytes".format(
                 h=host,
                 ns=namespace,
                 app=application) + "|awk '{print $2}'"
         pv_capacity = os.popen(pv_capacity_curl).read().strip()
         pv_utilization = os.popen(pv_utilization_curl).read().strip()
         logger.debug("PV utilisatin in bytes for pod running on host {hs} is {upv}".format(
                 hs=host,
                 upv=pv_utilization))
         if pv_capacity == "" or pv_utilization == "":
            failed_host.append(host)
            continue
         result.update({ "%s" % (host.strip()):(float(pv_utilization)/float(pv_capacity)) * 100})


    highutilization = 0
    failedhosts = 0
    resultkeypairexist = 0
    
    logger.debug("The % utilization of each pv hosted on paritcular host for application {app} and component {comp} in namespace {ns} is {rs}".format(
                app=application,
                comp=component,
                ns=namespace,
                rs=result))
    
    if result:
      resultkeypairexist = 1
      for hosts,percentage in result.items():
           if float(percentage) >= maxpercent:
              # for Prometheus exporter. When it has an error, this should print to file metrics. 
              # These metrix will be exported in prometheus
              # monitoring will be run like
              # ./pv_disk_utilization.py -a postgresql -co server -n ucp  > file
              print ("pv_high_utilization:{{namespace={ns},application={app},component={comp},host={hst},podname={podname},max_utilization={max_utilization},current_utilization={current_utilization}}} 0".format(
                  ns=namespace,
                  app=application,
                  comp=component,
                  hst=hosts,
                  podname=podname_host_keypair[hosts],
                  max_utilization=maxpercent,
                  current_utilization=percentage))
              highutilization = 1



    if len(failed_host) > 0:
        logger.error("Not able to determine pv utilization of {app} pods in namespace {ns} hosting on the host/hosts ".format(
                  app=application,
                  ns=namespace) + ", ".join(failed_host))
        failedhosts = 1


    if highutilization == 1 and failedhosts == 0 and resultkeypairexist == 1:
        return_code = CRITICAL
    elif highutilization == 0 and failedhosts == 1 and resultkeypairexist == 1:
        return_code = FAILEDHOST
    elif highutilization == 1 and failedhosts == 1 and resultkeypairexist == 1:
        return_code = CRITICAL
    elif highutilization == 0 and failedhosts == 0 and resultkeypairexist == 1:
        return_code = OK
    else:
        return_code=UNKNOWN

    return return_code



def main():
    # nagios monitoring
    # 0 - Service is OK.
    # 1 - service is not running on failed host
    # 2 - Service is in a CRITICAL status.
    # 3 - Service status is UNKNOWN

    # promotheus text file
    MAX_UTILIZATION = 80
    options = parse_args()
    setup_logging(options)
    if options.maxutilization:
       MAX_UTILIZATION = float(options.maxutilization.strip())
    logger.debug("checking pv utlization of pod {application} {component} in {namespace}".format(application=options.application,
                                                                                               component=options.component,
                                                                                               namespace=options.namespace))
    return_code = pv_utilization(options.application,options.component,options.namespace,MAX_UTILIZATION)
    sys.exit(return_code)

if __name__ == "__main__":
    main()
