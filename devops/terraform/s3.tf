resource "aws_s3_bucket" "assets" {
  bucket = "${var.project_name}-app-assets-production-2026"

  tags = {
    Name = "${var.project_name}-assets-bucket"
  }
}
