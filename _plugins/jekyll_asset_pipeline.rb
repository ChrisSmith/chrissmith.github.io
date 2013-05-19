require 'jekyll_asset_pipeline'
require 'colorize'

module JekyllAssetPipeline
  class LessConverter < JekyllAssetPipeline::Converter
    
    require 'less'

 	def self.filetype
      '.less'
    end
 
    def convert
      begin
        parser = Less::Parser.new()
        return parser.parse(@content).to_css
      rescue => e
        puts "Less Exception: #{e.message}".colorize(:red)
        return ""
      end
    end
  end
end