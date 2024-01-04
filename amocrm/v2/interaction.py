def _request(self, method, path, data=None, params=None, headers=None):
    print(f"_request - method: {method}")
    print(f"_request - data: {data}")

    # Проверка наличия данных
    if data:
        new_data = []
        for item in data:
            if 'note_type' in item and item['note_type'] == 'attachment':
                new_data.append({'note_type': item.pop('note_type'), item})
            else:
                new_data.append(item)
        print(f"_request - new_data: {new_data}")
    else:
        new_data = None

    headers = headers or {}
    headers.update(self.get_headers())

    try:
        response = self._session.request(method, url=self._get_url(path), json=new_data, params=params, headers=headers)
    except requests.exceptions.ConnectionError as e:
        raise exceptions.AmoApiException(e.args[0].args[0])  # Sometimes Connection aborted.

    if response.status_code == 204:
        return None, 204
    if response.status_code < 300 or response.status_code == 400:
        return response.json(), response.status_code
    if response.status_code == 401:
        raise exceptions.UnAuthorizedException()
    if response.status_code == 403:
        raise exceptions.PermissionsDenyException()
    if response.status_code == 402:
        raise ValueError("Тариф не позволяет включать покупателей")

    print(f"_request - response.text: {response.text}")
    raise exceptions.AmoApiException("Wrong status {} ({})".format(response.status_code, response.text))







