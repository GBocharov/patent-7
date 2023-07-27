from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer




def sum_all_shit(text : list, file_name = 'results.txt'):
    result = []
    try:
        tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-bigpatent")
        model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-bigpatent",max_length=150).to("cuda")

        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write('<<<<<<<< RESULT - 7 >>>>>>>>\n')
        for i in text:
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write('\n------------' + i[0] + '------------\n')
            s = sum_text(i[1], tokenizer, model, file_name)
            result.append([i[0], s])
        return result
    except:
        print(" Неверный формат данных ! ")
        return []

def split(tensor_dict, chunk_size = 4096):
    split_tensors = []
    for i in range(0, len(tensor_dict['input_ids'][0]), chunk_size):
        start = i
        end = i + chunk_size
        split_dict = {
            'input_ids': tensor_dict['input_ids'][:, start:end],
            'attention_mask': tensor_dict['attention_mask'][:, start:end]
        }
        #print(split_dict)
        if len(split_dict['input_ids'][0]) > 300:
            split_tensors.append(split_dict)
    return split_tensors

def sum_text(text, tokenizer, model, file_name):
    sumarizations = []
    inputs = tokenizer(text, return_tensors='pt')
    #print(inputs)
    inputs = split(inputs)
    print('chunk_num = ', len(inputs))
    for j, i in enumerate(inputs):
        for key, tensor in i.items():
            i[key] = tensor.to('cuda')
        #print(i)
        prediction = model.generate(**i, length_penalty = 0.8)
        prediction = tokenizer.batch_decode(prediction)
        print(prediction)
        sumarizations.append(prediction[0])

    with open('result.txt', 'a', encoding='utf-8') as f:
        for i in sumarizations:
            f.write('\n-->:'+ i)
    return sumarizations


