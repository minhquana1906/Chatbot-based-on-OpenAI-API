# Chatbot based on OpenAI API
## System Architecture
![](assets/Chatbot_based_on_OpenAI_API.drawio.png)

## Files Structure
```
.
├── app.py
├── assets
│   └── Chatbot_based_on_OpenAI_API.drawio.png
├── BuildJenkins-Dockerfile
├── data
│   ├── 1728149269.7578192-st_messages
│   ├── chats_history
│   └── None-st_messages
├── docker-compose.yaml
├── Dockerfile
├── helm
│   ├── model-serving
│   │   ├── Chart.yaml
│   │   ├── pvc.yaml
│   │   ├── pv.yaml
│   │   ├── templates
│   │   │   ├── deployment.yaml
│   │   │   ├── _helpers.tpl
│   │   │   ├── ingress.yaml
│   │   │   ├── NOTES.txt
│   │   │   └── service.yaml
│   │   └── values.yaml
│   ├── monitoring
│   │   ├── charts
│   │   │   ├── grafana
│   │   │   │   ├── Chart.yaml
│   │   │   │   ├── data-source-config.yaml
│   │   │   │   ├── templates
│   │   │   │   │   ├── config-map.yaml
│   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   ├── ingress.yaml
│   │   │   │   │   ├── NOTES.txt
│   │   │   │   │   └── service.yaml
│   │   │   │   └── values.yaml
│   │   │   ├── kubernetes-prometheus
│   │   │   │   ├── alert-config-map.yaml
│   │   │   │   ├── alert-deployment.yaml
│   │   │   │   ├── alert-service.yaml
│   │   │   │   ├── node-exporter-daemonset.yaml
│   │   │   │   ├── node-exporter-service.yaml
│   │   │   │   ├── prom-config-map.yaml
│   │   │   │   ├── prometheus-clusterRole.yaml
│   │   │   │   ├── prometheus-deployment.yaml
│   │   │   │   ├── prometheus-service.yaml
│   │   │   │   └── README.md
│   │   │   ├── loki-promtail
│   │   │   │   ├── loki-conf.yaml
│   │   │   │   └── promtail-conf.yaml
│   │   │   ├── opentelemetry-collector
│   │   │   │   ├── Chart.yaml
│   │   │   │   ├── ci
│   │   │   │   │   ├── clusterrole-values.yaml
│   │   │   │   │   ├── config-override-values.yaml
│   │   │   │   │   ├── daemonset-values.yaml
│   │   │   │   │   ├── deployment-values.yaml
│   │   │   │   │   ├── disabling-protocols-values.yaml
│   │   │   │   │   ├── GOMEMLIMIT-values.yaml
│   │   │   │   │   ├── hpa-deployment-values.yaml
│   │   │   │   │   ├── hpa-statefulset-values.yaml
│   │   │   │   │   ├── multiple-ingress-values.yaml
│   │   │   │   │   ├── networkpolicy-override-values.yaml
│   │   │   │   │   ├── networkpolicy-values.yaml
│   │   │   │   │   ├── preset-clustermetrics-values.yaml
│   │   │   │   │   ├── preset-hostmetrics-values.yaml
│   │   │   │   │   ├── preset-k8sevents-values.yaml
│   │   │   │   │   ├── preset-kubeletmetrics-values.yaml
│   │   │   │   │   ├── preset-kubernetesattributes-values.yaml
│   │   │   │   │   ├── preset-logscollection-values.yaml
│   │   │   │   │   ├── probes-values.yaml
│   │   │   │   │   └── statefulset-values.yaml
│   │   │   │   ├── CONTRIBUTING.md
│   │   │   │   ├── custom.yaml
│   │   │   │   ├── examples
│   │   │   │   │   ├── alternate-config
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── clusterrolebinding.yaml
│   │   │   │   │   │   │   ├── clusterrole.yaml
│   │   │   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── daemonset-and-deployment
│   │   │   │   │   │   ├── daemonset-values.yaml
│   │   │   │   │   │   ├── deployment-values.yaml
│   │   │   │   │   │   └── rendered
│   │   │   │   │   │       ├── configmap-agent.yaml
│   │   │   │   │   │       ├── configmap.yaml
│   │   │   │   │   │       ├── daemonset.yaml
│   │   │   │   │   │       ├── deployment.yaml
│   │   │   │   │   │       ├── serviceaccount.yaml
│   │   │   │   │   │       └── service.yaml
│   │   │   │   │   ├── daemonset-collector-logs
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-agent.yaml
│   │   │   │   │   │   │   ├── daemonset.yaml
│   │   │   │   │   │   │   └── serviceaccount.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── daemonset-hostmetrics
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-agent.yaml
│   │   │   │   │   │   │   ├── daemonset.yaml
│   │   │   │   │   │   │   └── serviceaccount.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── daemonset-lifecycle-hooks
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-agent.yaml
│   │   │   │   │   │   │   ├── daemonset.yaml
│   │   │   │   │   │   │   └── serviceaccount.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── daemonset-only
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-agent.yaml
│   │   │   │   │   │   │   ├── daemonset.yaml
│   │   │   │   │   │   │   └── serviceaccount.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── deployment-only
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── deployment-otlp-traces
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── deployment-use-existing-configMap
│   │   │   │   │   │   ├── deployment-values.yaml
│   │   │   │   │   │   └── rendered
│   │   │   │   │   │       ├── deployment.yaml
│   │   │   │   │   │       ├── serviceaccount.yaml
│   │   │   │   │   │       └── service.yaml
│   │   │   │   │   ├── kubernetesAttributes
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── clusterrolebinding.yaml
│   │   │   │   │   │   │   ├── clusterrole.yaml
│   │   │   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── README.md
│   │   │   │   │   ├── statefulset-only
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-statefulset.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   ├── service.yaml
│   │   │   │   │   │   │   └── statefulset.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── statefulset-with-pvc
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap-statefulset.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   ├── service.yaml
│   │   │   │   │   │   │   └── statefulset.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── using-custom-config
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   ├── using-GOMEMLIMIT
│   │   │   │   │   │   ├── rendered
│   │   │   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   │   │   └── service.yaml
│   │   │   │   │   │   └── values.yaml
│   │   │   │   │   └── using-shared-processes
│   │   │   │   │       ├── rendered
│   │   │   │   │       │   ├── configmap.yaml
│   │   │   │   │       │   ├── deployment.yaml
│   │   │   │   │       │   ├── serviceaccount.yaml
│   │   │   │   │       │   └── service.yaml
│   │   │   │   │       └── values.yaml
│   │   │   │   ├── README.md
│   │   │   │   ├── templates
│   │   │   │   │   ├── clusterrolebinding.yaml
│   │   │   │   │   ├── clusterrole.yaml
│   │   │   │   │   ├── configmap-agent.yaml
│   │   │   │   │   ├── configmap-statefulset.yaml
│   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   ├── _config.tpl
│   │   │   │   │   ├── daemonset.yaml
│   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   ├── _helpers.tpl
│   │   │   │   │   ├── hpa.yaml
│   │   │   │   │   ├── ingress.yaml
│   │   │   │   │   ├── networkpolicy.yaml
│   │   │   │   │   ├── NOTES.txt
│   │   │   │   │   ├── pdb.yaml
│   │   │   │   │   ├── podmonitor.yaml
│   │   │   │   │   ├── _pod.tpl
│   │   │   │   │   ├── prometheusrule.yaml
│   │   │   │   │   ├── serviceaccount.yaml
│   │   │   │   │   ├── servicemonitor.yaml
│   │   │   │   │   ├── service.yaml
│   │   │   │   │   └── statefulset.yaml
│   │   │   │   ├── UPGRADING.md
│   │   │   │   ├── values.schema.json
│   │   │   │   └── values.yaml
│   │   │   ├── secrets
│   │   │   │   └── chatbot-openai-1906-aee7016f9df4.json
│   │   │   └── tempo
│   │   │       ├── Chart.yaml
│   │   │       ├── custom.yaml
│   │   │       ├── README.md
│   │   │       ├── README.md.gotmpl
│   │   │       ├── templates
│   │   │       │   ├── configmap-tempo-query.yaml
│   │   │       │   ├── configmap-tempo.yaml
│   │   │       │   ├── _helpers.tpl
│   │   │       │   ├── ingress-tempo-query.yaml
│   │   │       │   ├── networkpolicy.yaml
│   │   │       │   ├── serviceaccount.yaml
│   │   │       │   ├── servicemonitor.yaml
│   │   │       │   ├── service.yaml
│   │   │       │   └── statefulset.yaml
│   │   │       └── values.yaml
│   │   ├── Chart.yaml
│   │   ├── templates
│   │   │   ├── deployment.yaml
│   │   │   ├── hpa.yaml
│   │   │   ├── ingress.yaml
│   │   │   ├── NOTES.txt
│   │   │   ├── serviceaccount.yaml
│   │   │   └── service.yaml
│   │   └── values.yaml
│   └── nginx-ingress
│       ├── Chart.yaml
│       ├── crds
│       │   ├── appprotectdos.f5.com_apdoslogconfs.yaml
│       │   ├── appprotectdos.f5.com_apdospolicy.yaml
│       │   ├── appprotectdos.f5.com_dosprotectedresources.yaml
│       │   ├── appprotect.f5.com_aplogconfs.yaml
│       │   ├── appprotect.f5.com_appolicies.yaml
│       │   ├── appprotect.f5.com_apusersigs.yaml
│       │   ├── externaldns.nginx.org_dnsendpoints.yaml
│       │   ├── k8s.nginx.org_globalconfigurations.yaml
│       │   ├── k8s.nginx.org_policies.yaml
│       │   ├── k8s.nginx.org_transportservers.yaml
│       │   ├── k8s.nginx.org_virtualserverroutes.yaml
│       │   └── k8s.nginx.org_virtualservers.yaml
│       ├── README.md
│       ├── templates
│       │   ├── clusterrolebinding.yaml
│       │   ├── clusterrole.yaml
│       │   ├── controller-configmap.yaml
│       │   ├── controller-daemonset.yaml
│       │   ├── controller-deployment.yaml
│       │   ├── controller-globalconfiguration.yaml
│       │   ├── controller-hpa.yaml
│       │   ├── controller-ingress-class.yaml
│       │   ├── controller-leader-election-configmap.yaml
│       │   ├── controller-pdb.yaml
│       │   ├── controller-prometheus-service.yaml
│       │   ├── controller-rolebinding.yaml
│       │   ├── controller-role.yaml
│       │   ├── controller-secret.yaml
│       │   ├── controller-serviceaccount.yaml
│       │   ├── controller-servicemonitor.yaml
│       │   ├── controller-service.yaml
│       │   ├── controller-wildcard-secret.yaml
│       │   ├── _helpers.tpl
│       │   └── NOTES.txt
│       ├── values-icp.yaml
│       ├── values-nsm.yaml
│       ├── values-plus.yaml
│       ├── values.schema.json
│       └── values.yaml
├── iac
│   ├── ansible
│   │   ├── inventory
│   │   ├── playbooks
│   │   │   ├── create_compute_instances.yaml
│   │   │   └── deploy_jenkins.yaml
│   │   └── secrets
│   │       └── chatbot-openai-1906-43a7fb0b56ea.json
│   ├── requirements.txt
│   └── terraform
│       ├── main.tf
│       ├── terraform.tfstate
│       ├── terraform.tfstate.backup
│       └── variables.tf
├── Jenkinsfile
├── Makefile
├── note.txt
├── README.md
└── requirements.txt
```