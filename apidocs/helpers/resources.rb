require 'middleman-syntax'

module Resources
  module Helpers

    STATUSES ||= {
      200 => '200 OK',
      201 => '201 Created',
      202 => '202 Accepted',
      204 => '204 No Content',
      205 => '205 Reset Content',
      301 => '301 Moved Permanently',
      302 => '302 Found',
      307 => '307 Temporary Redirect',
      304 => '304 Not Modified',
      401 => '401 Unauthorized',
      403 => '403 Forbidden',
      404 => '404 Not Found',
      405 => '405 Method not allowed',
      409 => '409 Conflict',
      422 => '422 Unprocessable Entity',
      500 => '500 Server Error',
      502 => '502 Bad Gateway'
    }

    def json(key)
      hash = get_resource(key)
      hash = yield hash if block_given?
      Middleman::Syntax::Highlighter.highlight(JSON.pretty_generate(hash), 'json').html_safe
    end

    def get_resource(key)
      hash = case key
        when Hash
          h = {}
          key.each { |k, v| h[k.to_s] = v }
          h
        when Array
          key
        else Resources.const_get(key.to_s.upcase)
      end
      hash
    end

    def text_html(response, status, head = {})
      hs = headers(status, head.merge('Content-Type' => 'text/html'))
      res = CGI.escapeHTML(response)
      hs + %(<pre class="body-response"><code>) + res + "</code></pre>"
    end

  end

  AUTH_TOKEN ||= {
    token: "lkja8*lkajsd*lkjas;ldkj8asd;kJASd811"
  }

  CARD ||= {
      id: 1,
      owner_type: 'parent',
      owner_id: 2,
      name_on_card: 'Moira Ripley',
      number: '4856200001123821',
      expiration_date: '2018-06-01',
      type: 'C',
      sub_type: 'R',
      amount_on_card: '0.00',
      amount_spent: '0.00'
  }

  CHORE ||= {
      id: 1,
      kid: 1,
      name: 'Take out the trash',
      points: '34',
      status: 'incomplete'
  }

  KID ||= {
      id: 1,
      name: 'John Timmy',
      avatar: {
          'full_size': 'https://johnsonandjohnson.com/me.jpg'
      }
  }

  RULE ||= {
      id: 1,
      type: 'merchant',
      merchant_types: [
          'MCT_RECREATION',
          'MCT_ELECTRONICS',
      ]
  }

  TRANSACTION ||= {
      id: 1,
      card: 1,
      amount: '35.25',
      merchant_name: 'Costco',
      status: 'approved',
      when: '2016-09-10T12:34:12'
  }

  USER ||= {
    id: 1,
    email: 'john@gmail.com',
    parent: {
        id: 2,
        'first_name': 'John',
        'last_name': 'Ripley',
        'avatar': {
            'full_size': 'https://google.ca/image.png'
        }
    }
  }

end

include Resources::Helpers
