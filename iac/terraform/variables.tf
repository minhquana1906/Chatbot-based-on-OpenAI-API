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
