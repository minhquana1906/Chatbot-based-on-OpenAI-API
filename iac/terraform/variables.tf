variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "chatbot-openai-1906"
}

variable "region" {
  description = "The region the cluster in"
  default     = "asia-southeast1"
}

variable "zone" {
  description = "The zone the cluster in"
  default     = "asia-southeast1-a"
}

variable "bucket-loki" {
  description = "Bucket for loki to store logs"
  default     = "logs-by-loki"
}

variable "bucket-tempo" {
  description = "Bucket for tempo to store logs"
  default     = "traces-by-tempo"
}

variable "bucket-prometheus" {
  description = "Bucket for prometheus to store metrics"
  default     = "metrics-by-prometheus"
}